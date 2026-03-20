from typing import List, Tuple
from collections import deque, defaultdict

def has_deadlock(num_tasks: int, dependencies: List[Tuple[int, int]]) -> bool:
    """
    Detects if a circular dependency (deadlock) exists in an AI agent workflow.
    Uses Kahn's Algorithm for Topological Sorting.
    Complexity: O(V + E) time | O(V + E) space.
    """
    if num_tasks <= 0:
        return False

    # 1. Initialize Graph and In-Degree array - O(V)
    graph = defaultdict(list)
    in_degree = {i: 0 for i in range(num_tasks)}

    # 2. Build the Graph (prerequisite -> task) - O(E)
    for prereq, task in dependencies:
        graph[prereq].append(task)
        in_degree[task] += 1

    # 3. Initialize Queue with independent tasks
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    processed_tasks = 0

    # 4. Process the queue (Topological Sort) - O(V + E)
    while queue:
        current = queue.popleft()
        processed_tasks += 1

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If we couldn't process all tasks, a cycle (deadlock) exists
    return processed_tasks != num_tasks
