from collections import deque


def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    """
    Breadth-First Search to find augmenting paths in the residual graph.

    Args:
        capacity_matrix: Matrix of edge capacities
        flow_matrix: Matrix of current flows
        source: Source node index
        sink: Sink node index
        parent: Array to store the augmenting path

    Returns:
        True if there is an augmenting path from source to sink, False otherwise
    """
    num_nodes = len(capacity_matrix)
    visited = [False] * num_nodes
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(num_nodes):
            # Check if there is residual capacity in the edge
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False

def edmonds_karp(capacity_matrix, source, sink):
    """
    Edmonds-Karp algorithm to find the maximum flow in a network.

    Args:
        capacity_matrix: Matrix of edge capacities
        source: Source node index
        sink: Sink node index

    Returns:
        max_flow: Maximum flow value
        flow_matrix: Matrix of flows
    """
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0

    # While there is an augmenting path, add flow
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Find the minimum residual capacity along the augmenting path
        path_flow = float('inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node

        # Update the flow along the augmenting path
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow  # Reverse edge for residual graph
            current_node = previous_node

        max_flow += path_flow

    return max_flow, flow_matrix
