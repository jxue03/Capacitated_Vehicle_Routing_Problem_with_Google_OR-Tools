# Capacitated Vehicle Routing Problems solved with Google OR-Tools

This project implements and evaluates the **Capacitated Vehicle Routing Problem (CVRP)** using Google OR-Tools. Standard benchmark instances from CVRPLIB are used to evaluate different first-solution strategies and local-search metaheuristics.

The goal of the project is to explore how different OR-Tools routing strategies affect solution quality across CVRP instances of varying sizes and structures.

## Problem Description

The Capacitated Vehicle Routing Problem determines a set of vehicle routes that serve all customers while minimizing total travel distance.

The model requires that:

- Each customer is visited exactly once.
- Each route starts and ends at the depot.
- The total demand assigned to a vehicle does not exceed its capacity.
- Total travel distance across all vehicle routes is minimized.

## Dataset

Benchmark instances are obtained from **CVRPLIB**.

Six instances from the A, B, and X sets are evaluated:

| Instance | # Customers | # Vehicles | Vehicle Capacity | Total Fleet Capacity | Total Demand | Unused Capacity | 
|---|---:|---:|---:|---:|---:|---|
| A-n48-k7 | 47 | 7 | 100 | 700 | 626 | 74 |
| A-n65-k9 | 64 | 9 | 100 | 900 | 877 | 23 |
| B-n41-k6 | 40 | 6 | 100 | 600 | 567 | 33 |
| B-n68-k9 | 67 | 9 | 100 | 900 | 837 | 63 |
| X-n110-k13 | 109 | 13 | 66 | 858 | 816 | 42 |
| X-n129-k18 | 128 | 18 | 39 | 702 | 665 | 37 |

A sets are...
B sets are...
X sets are...

## OR-Tools Implementation

The CVRP is implemented using the OR-Tools Routing Solver.

The implementation includes:

- `RoutingIndexManager` for mapping between routing and problem indices
- `RoutingModel` for constructing the routing problem
- A distance callback for arc costs
- A demand callback for customer demands
- A capacity dimension for enforcing vehicle capacity constraints
- Configurable first-solution and local-search strategies
- Solution validation for total demand and route feasibility

Travel distances from CVRPLIB are rounded using the TSPLIB metric rounding convention.

## Search Algorithms

Each instances are evaluated in two stages: first-solution construction heuristics and local-search metaheuristics.
Google OR-Tools provides a broad range of search strategies; however, this study mainly focuses on four relevant first-solution strategies:   
- `PATH_CHEAPEST_ARC`: Starting froma route "start" node, conect it to the node which produces the cheapest route segment, then extend the route by iterating on the last node added to the route.   
- `PARALLEL_CHEAPEST_INSERTION`: Iteratively build a solution by inserting the cheapest node at its cheapest position; the cost of insertion is based on the arc cost function.
- `LOCAL_CHEAPEST_INSERTION`: Iteratively build a solution by inserting each node at its cheapest position; the cost of insertion is based on the arc cost function.
- `SAVINGS`: Saving algorithm (Clarke & Wright).
   
and three local-search metaheuristics:  
- `GUIDED_LOCAL_SEARCH`
- `TABU_SEARCH`
- `SIMULATED_ANNEALING`



The underlying CVRP formulation and computational settings were kept fixed while search strategies were varied.


| A-n48-k7 | `Guided Local Search` | `Tabu Local Search` | `Simulated Annealing` |
|---|---:|---:|---|
| `Parallel Cheapest Insertion` | 1088 | 1116 | 1152 | 
| `Path Cheapest Arc` | **1073** | 1102 | 1221 |
| `Savings` | **1073** | 1097 | 1097 | 
| `Local Cheapest Insertion` | 1084 | 1127 | 1192 |

## Results

Solution quality is evaluated relative to the published best-known solution (BKS) for each CVRPLIB instance.
 
       
| Instance | Best Known Solution (BKS) | Best OR-Tools Solution | Optimality Gap | Best Configuration |
|---|---:|---:|---:|---|
| A-n48-k7 | 1073 | 1073 | 0.00% | `Path Cheapest Arc` or `Savings` + `Guided Local Search` |
| A-n65-k9 | 1174 | 1184 | 0.85% | `Parallel Cheapest Insertion` or `Local Cheapest Insertion` + `Guided Local Search` |
| B-n41-k6 | 829 | 829 | 0.00% | `Path Cheapest Arc` or `Local Cheapest Insertion` + `Guided Local Search` |
| B-n68-k9 | 1272 | 1289 | ~1.34% | `Parallel Cheapest Insertion` or `Path Cheapest Arc` + `Guided Local Search`|
| X-n110-k13 | 14971 | 15150 | ~1.20% | `Local Cheapest Insertion` + `Guided Local Search` |
| X-n129-k18 | 28940 | 30161 | ~4.22% | `Parallel Cheapest Insertion` + `Guided Local Search` |

The optimality gap is calculated as:

**Gap (%) = (OR-Tools Solution - BKS) / BKS × 100**

Across the five tested instances, OR-Tools matched the best-known solution on three instances and produced solutions within approximately 1% of the BKS on the remaining two.

## Key Findings

**Guided Local Search performed consistently well.**  
Across the tested instances and search configurations, `GUIDED_LOCAL_SEARCH` produced better final solutions than `TABU_SEARCH` and `SIMULATED_ANNEALING` under the same computational settings.

**The first-solution strategy still affected final solution quality.**  
Different construction heuristics sometimes led to different final solutions even after local search. For example, on `A-n65-k9`, both Parallel Cheapest Insertion and Global Cheapest Arc combined with Guided Local Search reached a distance of 1184, while Savings combined with Guided Local Search reached 1195.

**Different initial solutions can converge to the same final solution.**  
The identical 1184 result from multiple construction strategies on `A-n65-k9` suggests that Guided Local Search can move different initial solutions toward the same high-quality local optimum.

## Project Structure

```text
cvrp-ortools/
│
├── import packages and solver
│
├── read instance/
│   ├── A-n48-k7.vrp
│   ├── A-n65-k9.vrp
│   ├── B-n41-k6.vrp
│   ├── B-n68-k9.vrp
│   ├── X-n110-k13.vrp
│   └── X-n129-k18.vrp
│
├── create_data_model
│
├── print instance summary
│
├── build_routing_model/
│   ├── create RoutingIndexManager
│   ├── distance_callback
│   └── demand_callback
│
├── create_search_parameters/
│   ├── first_solution_strategy 
│   └── local_search_metaheuristic
│
├── set time limit
├── print routing status
│
└── results/
    ├── print solution
    ├── plot the routes
    └── print optimality gap
```
