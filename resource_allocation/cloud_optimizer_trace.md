# Reasoning Trace: Optimal Cloud Resource Allocator

## 1. Problem Context & Objective
During periods of high traffic or intensive incident response, an orchestration system must spin up various cloud compute clusters. Each cluster has a specific financial `cost` and provides a specific amount of `compute_power`. 

**The core constraint:** We have a strict `max_budget`. We need to select a combination of clusters that maximizes total compute power without exceeding the budget. A cluster can either be provisioned or not (0/1 binary choice).

## 2. Approach 1: The Naive Method (Recursive Branching)
The brute-force method evaluates every possible combination of clusters by either including or excluding each one and tracking the remaining budget.
* **Time Complexity:** $O(2^N)$ where $N$ is the number of available clusters.
* **Why it fails at scale:** Exponential time complexity means that evaluating even 50 different cluster options would take billions of operations. The orchestrator would time out before making a deployment decision.

## 3. Approach 2: The Production Method (Dynamic Programming - Space Optimized)
This is a variation of the classic 0/1 Knapsack problem. We use **Dynamic Programming (DP)** to build up the optimal solution systematically. 

A standard DP approach uses a 2D matrix of size `N x Budget`, but we optimize this to a **1D Array** to save memory, which is critical when running inside lightweight containerized environments.

1. **Initialization:** We create an array `dp` of size `max_budget + 1`, initialized to 0. `dp[i]` represents the maximum compute power achievable with budget `i`.
2. **Backwards Traversal:** As we iterate through each available cluster, we update the `dp` array from the `max_budget` down to the cluster's `cost`. Traversing backwards ensures we only evaluate each cluster once per budget state (preventing infinite loops of reusing the same cluster).

* **Time Complexity:** $O(N \times B)$ where $N$ is the number of clusters and $B$ is the `max_budget`. 
* **Space Complexity:** $O(B)$ for the 1D array.
* **Why this is the right choice:** By trading exponential time complexity for pseudo-polynomial time, we guarantee a fast, deterministic resolution. The 1D space optimization ensures the memory footprint remains tiny.

## 4. Edge Cases Handled
* **Zero Budget / Empty Arrays:** Instantly returns 0, avoiding unnecessary loop initializations.
* **Mismatched Input Lengths:** Raises a fast `ValueError` to prevent silent calculation errors if the telemetry data pipeline is corrupted.
