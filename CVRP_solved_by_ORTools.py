"""Capacited Vehicles Routing Problem (CVRP)."""

import vrplib
import numpy as np

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Read the VRP instance
# note that this code is currently importing instance "A-n65-k9" with "PARALLEL_CHEAPEST_INSERTION" and "GUIDED_LOCAL_SEARCH".
# it can be modified using other instances, solutions, first-solution strategies, and local-search metaheuristics.
instance = vrplib.read_instance(r"C:\Users\Jenny\Downloads\A-n65-k9.vrp")

# Read the VRP instance best known solution
best_known_solution = vrplib.read_solution(r"C:\Users\Jenny\Downloads\A-n65-k9.sol")

# convert the CVRPLIB instance into the data format
def create_data_model(instance, num_vehicles):
    data = {}

    # Distance matrix
    # (round using TSPLIB Metric Rounding Function)
    data["distance_matrix"] = np.floor(
        instance["edge_weight"] + 0.5
    ).astype(np.int64)

    # Customer demands
    data["demands"] = instance["demand"].astype(np.int64)

    # Number of vehicles
    data["num_vehicles"] = num_vehicles

    # Capacity of each vehicle
    vehicle_capacity = int(instance["capacity"])
    data["vehicle_capacities"] = [vehicle_capacity] * num_vehicles

    # Depot (already converted to 0-based indexing by vrplib)
    data["depot"] = int(instance["depot"][0])

    return data

data = create_data_model(
    instance,
    num_vehicles = 9
)

# print current set's key features
print(instance.keys())
print("Number of customers:", len(data["demands"]) - 1)  # exclude depot
print("Number of vehicles:", data["num_vehicles"])
print("Vehicle capacity:", data["vehicle_capacities"][0])
print("Total fleet capacity:", sum(data["vehicle_capacities"]))
print("Total demand:", data["demands"].sum())
print("Unused capacity:", 
      sum(data["vehicle_capacities"]) - data["demands"].sum())
print("Maximum customer demand:", data["demands"].max())


# create routing manager and model
def build_routing_model(data):
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]),
        data["num_vehicles"],
        data["depot"]
    )
    routing = pywrapcp.RoutingModel(manager)

    # Define and register the distance callback.
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(
            data["distance_matrix"][from_node, to_node]
        )

    transit_callback_index = routing.RegisterTransitCallback(
        distance_callback
    )
    routing.SetArcCostEvaluatorOfAllVehicles(
        transit_callback_index
    )

    # Define and register the demand callback and capacity constraint.
    def demand_callback(from_index):
        node = manager.IndexToNode(from_index)
        return int(data["demands"][node])

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback
    )

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        data["vehicle_capacities"],
        True,
        "Capacity"
    )

    return manager, routing

manager, routing = build_routing_model(data)

# create search parameters
def create_search_parameters():
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )

    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )

    search_parameters.time_limit.seconds = 60
    search_parameters.log_search = False

    return search_parameters


search_parameters = create_search_parameters()
solution = routing.SolveWithParameters(search_parameters)
status = routing.status()

print("Routing status code:", status)
status_messages = {
    0: "ROUTING_NOT_SOLVED",
    1: "ROUTING_SUCCESS",
    2: "ROUTING_PARTIAL_SUCCESS_LOCAL_OPTIMUM_NOT_REACHED",
    3: "ROUTING_FAIL",
    4: "ROUTING_FAIL_TIMEOUT",
    5: "ROUTING_INVALID",
    6: "ROUTING_INFEASIBLE",
}

print("Routing status:", status_messages.get(status, "UNKNOWN"))

if solution is None:
    print("OR-Tools did not return a solution.")
else:
    print("A feasible solution was found.")
    print("Objective value:", solution.ObjectiveValue())

# print solution
def print_solution(data, manager, routing, solution):
    """Print routes, cumulative loads, route distances, and totals."""

    print("=" * 50)
    print(f"Objective value: {solution.ObjectiveValue()}")
    print("=" * 50)

    total_distance = 0
    total_load = 0
    used_vehicles = 0
    routes = []

    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue

        used_vehicles += 1
        index = routing.Start(vehicle_id)

        route_nodes = []
        route_distance = 0
        route_load = 0
        route_parts = []

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route_nodes.append(node)

            route_load += int(data["demands"][node])
            route_parts.append(f"{node} Load({route_load})")

            previous_index = index
            index = solution.Value(routing.NextVar(index))

            route_distance += routing.GetArcCostForVehicle(
                previous_index,
                index,
                vehicle_id,
            )

        end_node = manager.IndexToNode(index)
        route_nodes.append(end_node)
        route_parts.append(f"{end_node} Load({route_load})")

        print(f"\nRoute for vehicle {vehicle_id}:")
        print(" -> ".join(route_parts))
        print(f"Distance of the route: {route_distance}")
        print(f"Load of the route: {route_load}")

        routes.append(route_nodes)
        total_distance += route_distance
        total_load += route_load

    expected_demand = int(data["demands"].sum())

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("Used vehicles:", used_vehicles)
    print("Total distance:", total_distance)
    print("Total delivered demand:", total_load)
    print("Expected total demand:", expected_demand)
    print("Capacity per vehicle:", data["vehicle_capacities"][0])

    print(
        "Demand check:",
        "PASSED" if total_load == expected_demand else "FAILED",
    )
    print(
        "Objective check:",
        "PASSED"
        if total_distance == solution.ObjectiveValue()
        else "CHECK REQUIRED",
    )
    return routes

if solution is not None:
    routes = print_solution(data, manager, routing, solution)


# calculate the optimality gap between ortools and best_known_solution
bks_distance = best_known_solution["cost"]
gap = (solution.ObjectiveValue() - bks_distance) / bks_distance * 100
print(f"Optimality gap: {gap:.2f}%")
