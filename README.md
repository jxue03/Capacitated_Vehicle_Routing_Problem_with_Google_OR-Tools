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
| X-n110-k13 | 40 | 6 | 66 | 858 | 816 | 42 |
| X-n129-k18 | 67 | 9 | 39 | 702 | 665 | 37 |

`A-n33-k6` is used as a small validation instance, while the remaining instances provide the primary performance comparison.

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

## Search Strategies

Several first-solution strategies were evaluated, including:

- `PATH_CHEAPEST_ARC`
- `PARALLEL_CHEAPEST_INSERTION`
- `LOCAL_CHEAPEST_INSERTION`
- `SAVINGS`
- `GLOBAL_CHEAPEST_ARC`

The following local-search metaheuristics were also compared:

- `GUIDED_LOCAL_SEARCH`
- `TABU_SEARCH`
- `SIMULATED_ANNEALING`

The underlying CVRP formulation and computational settings were kept fixed while search strategies were varied.

## Results

Solution quality is evaluated relative to the published best-known solution (BKS) for each CVRPLIB instance.

| Instance | BKS | Best OR-Tools Solution | Optimality Gap | Best Configuration |
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
├── README.md
├── requirements.txt
│
├── data/
│   ├── A-n33-k6.vrp
│   ├── A-n48-k7.vrp
│   ├── A-n65-k9.vrp
│   ├── B-n41-k6.vrp
│   └── B-n68-k9.vrp
│
├── src/
│   ├── cvrp_solver.py
│   └── experiments.py
│
└── results/
    └── benchmark_results.csv
```

## Technologies

- Python
- Google OR-Tools
- NumPy
- vrplib
- CVRPLIB benchmark instances

## Future Work

Possible extensions include:

- Testing larger CVRPLIB instances
- Evaluating the effect of different computational time limits
- Visualizing vehicle routes
- Investigating more advanced routing variants such as VRPTW
