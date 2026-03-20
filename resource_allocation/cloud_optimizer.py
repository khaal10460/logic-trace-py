from typing import List

def optimize_cluster_allocation(costs: List[int], compute_power: List[int], max_budget: int) -> int:
    """
    Calculates the maximum compute power achievable within a strict cloud budget.
    Uses 1D Dynamic Programming (0/1 Knapsack optimization).
    Complexity: O(N * B) time | O(B) space, where N is tasks and B is max_budget.
    """
    if not costs or not compute_power or max_budget <= 0:
        return 0
        
    n = len(costs)
    if n != len(compute_power):
        raise ValueError("Mismatch between costs and compute power arrays.")

    # 1D DP array to store the max compute power for every budget up to max_budget.
    # We optimize space complexity from O(N * B) to O(B).
    dp = [0] * (max_budget + 1)

    for i in range(n):
        cost = costs[i]
        power = compute_power[i]
        
        # Traverse backwards to prevent using the same compute cluster multiple times
        for current_budget in range(max_budget, cost - 1, -1):
            dp[current_budget] = max(dp[current_budget], dp[current_budget - cost] + power)

    return dp[max_budget]
