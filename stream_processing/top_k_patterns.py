import heapq
from collections import Counter
from typing import List

def top_k_suspicious_patterns(stream: List[str], k: int) -> List[str]:
    """
    Solves the Top K Frequent Elements problem using a Min-Heap.
    Complexity: O(N log K) time | O(N) space
    """
    if not stream or k <= 0:
        return []

    # 1. Frequency Map - O(N)
    counts = Counter(stream)

    # 2. Min-Heap of size K - O(N log K)
    # We use a Min-Heap so the least frequent element is always at the root for easy removal.
    return heapq.nlargest(k, counts.keys(), key=counts.get)
