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

## OR-Tools Implementation and Project Structure

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

```text
CVRP_solved_by_ORtools.py
│
├── Load CVRPLIB instance
│
├── Create data model
│
├── Build routing model
│   ├── RoutingIndexManager
│   ├── Distance callback
│   └── Demand / capacity constraints
│
├── Configure search
│   ├── First-solution strategy
│   ├── Local-search metaheuristic
│   └── Time limit
│
├── Solve
│
└── Process results
    ├── Print solution
    ├── Plot routes
    └── Calculate BKS gap
```

                          
## Search Algorithms

Each CVRP instance is evaluated in two stages: a first-solution construction heuristic generates an initial feasible solution, followed by a local-search metaheuristic that improves the solution.
                   
Although Google OR-Tools provides a broad range of first-solution strategies, this study focuses on four representative and competitive construction heuristics selected to capture distinct route-construction approaches: greedy path construction, parallel and sequential insertion, and savings-based route construction:
      
- `PATH_CHEAPEST_ARC`: Start from a route "start" node, constructs routes sequentially by repeatedly extending the current route through the cheapest feasible arc. It represents a greedy, path-based construction approach.
     
- `PARALLEL_CHEAPEST_INSERTION`: Builds multiple routes simultaneously by repeatedly selecting low-cost feasible customer insertions across the developing routes. It represents a parallel insertion-based approach.
    
- `LOCAL_CHEAPEST_INSERTION`: Considers customers sequentially and inserts each customer into its cheapest feasible position among the existing routes. It provides a sequential insertion-based alternative to PCI.
         
- `SAVINGS`: A savings-based construction approach inspired by the Clarke-Wright Savings algorithm. Routes are formed by prioritizing combinations that reduce travel cost relative to serving customers separately from the depot.
   
Three local-search metaheuristics are then evaluated for improving the constructed solutions:
          
- `GUIDED_LOCAL_SEARCH`: Escapes local optima by dynamically penalizing costly solution features, encouraging the search to explore alternative regions of the solution space.
            
- `TABU_SEARCH`: Uses short-term search memory to temporarily restrict recently used moves, reducing cycling and encouraging exploration beyond the current local optimum.
                   
- `SIMULATED_ANNEALING`: Probabilistically accepts some worsening moves, particularly earlier in the search, to escape local optima and explore alternative solutions.
           
Preliminary experimentation indicated that these strategies performed competitively across the selected CVRPLIB instances. Other strategies were explored during initial testing but were excluded from the final benchmark to keep the analysis manageable, as they offered limited additional methodological diversity, were less consistently competitive, or were less relevant to the scope of the study.
       
## Results
                  
`Guided Local Search` demonstrated the most consistent performance across the tested instances, suggesting greater robustness than `Tabu Search` and `Simulated Annealing` under the experimental settings. As a representative example, the table below presents the local-search comparison for A-n48-k7. Similar comparisons were conducted across all benchmark instances, with Guided Local Search consistently producing the strongest results.
   
| A-n48-k7 | `Guided Local Search` | `Tabu Local Search` | `Simulated Annealing` |
|---|---:|---:|---|
| `Parallel Cheapest Insertion` | 1088 | 1116 | 1152 | 
| `Path Cheapest Arc` | **1073** | 1102 | 1221 |
| `Savings` | **1073** | 1097 | 1097 | 
| `Local Cheapest Insertion` | 1084 | 1127 | 1192 |

After the local-search metaheuristics is set to `Guided Local Search`, first-solution construction heuristics are also evaluated across all instances.       
The best solutions are highlighted in bold. 
     
| Instances | A-n48-k7 | A-n65-k9 | B-n41-k6 | B-n68-k9 | X-n110-k13 | X-n129-k18 |
|---|---:|---:|---:|---:|---:|---|
| `Parallel Cheapest Insertion` | 1088 | **1184** | 843 | 1290 | 15449 | **30161** | 
| `Path Cheapest Arc` | **1073** | 1218 | **829** | **1289** | 15260 | 30506 | 
| `Savings` | **1073** | 1195 | 840 | 1307 | 15554 | 30889 | 
| `Local Cheapest Insertion` | 1084 | **1184** | **829** | 1311 | **15150** | 30970 | 

Then the best found solution are evaluated relative to the published best-known solution (BKS) for each CVRPLIB instance.
                        
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
