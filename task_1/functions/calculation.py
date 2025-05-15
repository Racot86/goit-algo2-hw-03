def create_capacity_matrix(G, node_mapping):
    num_nodes = len(node_mapping)
    capacity_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    for u, v, data in G.edges(data=True):
        u_idx = node_mapping[u]
        v_idx = node_mapping[v]
        capacity_matrix[u_idx][v_idx] = data['capacity']

    return capacity_matrix

def calculate_terminal_to_store_flow(G, flow_matrix, node_mapping):
    terminal_store_flow = {}

    terminals = [node for node in G.nodes() if G.nodes[node].get('type') == 'terminal']
    stores = [node for node in G.nodes() if G.nodes[node].get('type') == 'store']

    for terminal in terminals:
        for store in stores:
            paths = []
            for warehouse in [node for node in G.nodes() if G.nodes[node].get('type') == 'warehouse']:
                if G.has_edge(terminal, warehouse) and G.has_edge(warehouse, store):
                    paths.append((terminal, warehouse, store))

            total_flow = 0
            for path in paths:
                t, w, s = path
                t_idx = node_mapping[t]
                w_idx = node_mapping[w]
                s_idx = node_mapping[s]

                path_flow = min(flow_matrix[t_idx][w_idx], flow_matrix[w_idx][s_idx])
                total_flow += path_flow

            if total_flow > 0:
                terminal_store_flow[(terminal, store)] = total_flow

    return terminal_store_flow
