from task_1.functions.input import create_logistics_network
from task_1.functions.utility import edmonds_karp
from task_1.functions.calculation import create_capacity_matrix, calculate_terminal_to_store_flow
from task_1.functions.output import generate_report, visualize_network



def main():
    G = create_logistics_network()

    nodes = list(G.nodes())
    node_mapping = {node: i for i, node in enumerate(nodes)}
    reverse_mapping = {i: node for node, i in node_mapping.items()}

    capacity_matrix = create_capacity_matrix(G, node_mapping)

    source_idx = node_mapping['source']
    sink_idx = node_mapping['sink']

    max_flow, flow_matrix = edmonds_karp(capacity_matrix, source_idx, sink_idx)

    terminal_store_flow = calculate_terminal_to_store_flow(G, flow_matrix, node_mapping)

    generate_report(G, max_flow, terminal_store_flow, node_mapping, flow_matrix)

    visualize_network(G, flow_matrix, node_mapping)

    print(f"Maximum flow: {max_flow} units")
    print("Network flow visualization will be displayed in a separate window")

if __name__ == '__main__':
    main()
