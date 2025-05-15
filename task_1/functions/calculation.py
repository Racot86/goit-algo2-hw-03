def create_capacity_matrix(G, node_mapping):
    """
    Create a capacity matrix from the networkx graph.

    Args:
        G: NetworkX graph
        node_mapping: Dictionary mapping node names to indices

    Returns:
        capacity_matrix: Matrix of edge capacities
    """
    num_nodes = len(node_mapping)
    capacity_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    for u, v, data in G.edges(data=True):
        u_idx = node_mapping[u]
        v_idx = node_mapping[v]
        capacity_matrix[u_idx][v_idx] = data['capacity']

    return capacity_matrix

def calculate_terminal_to_store_flow(G, flow_matrix, node_mapping):
    """
    Calculate the flow from terminals to stores.

    Args:
        G: NetworkX graph
        flow_matrix: Matrix of flows
        node_mapping: Dictionary mapping node names to indices

    Returns:
        terminal_store_flow: Dictionary with terminal-store pairs as keys and flow values
    """
    terminal_store_flow = {}

    # Get all terminals and stores
    terminals = [node for node in G.nodes() if G.nodes[node].get('type') == 'terminal']
    stores = [node for node in G.nodes() if G.nodes[node].get('type') == 'store']

    # For each terminal-store pair, find all paths and sum the flows
    for terminal in terminals:
        for store in stores:
            # Find all paths from terminal to store
            paths = []
            for warehouse in [node for node in G.nodes() if G.nodes[node].get('type') == 'warehouse']:
                if G.has_edge(terminal, warehouse) and G.has_edge(warehouse, store):
                    paths.append((terminal, warehouse, store))

            # Calculate flow for each path
            total_flow = 0
            for path in paths:
                t, w, s = path
                t_idx = node_mapping[t]
                w_idx = node_mapping[w]
                s_idx = node_mapping[s]

                # The flow is the minimum of the flows on the two edges
                path_flow = min(flow_matrix[t_idx][w_idx], flow_matrix[w_idx][s_idx])
                total_flow += path_flow

            if total_flow > 0:
                terminal_store_flow[(terminal, store)] = total_flow

    return terminal_store_flow
