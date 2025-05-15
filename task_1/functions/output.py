import networkx as nx
from matplotlib import pyplot as plt


def generate_report(G, max_flow, terminal_store_flow, node_mapping, flow_matrix):
    print("Аналіз потоків у логістичній мережі")
    print("==================================\n")

    print(f"Максимальний потік: {max_flow} одиниць\n")

    print("Таблиця потоків від терміналів до магазинів:")
    print("-------------------------------------------")
    print("Термінал\tМагазин\tПотік (од.)")

    for (terminal, store), flow in sorted(terminal_store_flow.items()):
        print(f"{terminal}\t{store}\t{flow}")

    print()

    terminal_flow = {}
    for (terminal, _), flow in terminal_store_flow.items():
        terminal_flow[terminal] = terminal_flow.get(terminal, 0) + flow

    print("Питання для аналізу:")
    print("--------------------")

    print("1. Які термінали забезпечують найбільший потік до магазинів?")
    for terminal, flow in sorted(terminal_flow.items(), key=lambda x: x[1], reverse=True):
        print(f"   {terminal}: {flow} од.")

    print()

    print("2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?")
    min_capacity_edges = [
        (u, v, data['capacity'])
        for u, v, data in G.edges(data=True)
        if 'capacity' in data and data['capacity'] < float('inf')
    ]
    min_capacity_edges.sort(key=lambda x: x[2])

    for u, v, capacity in min_capacity_edges[:5]:
        print(f"   {u} → {v}: {capacity} од.")

    print("\n   Ці «вузькі горлечка» обмежують пропускну здатність усієї мережі.\n")

    print("3. Які магазини отримали найменше товару і чи можна збільшити їх постачання?")
    store_flow = {}
    for (_, store), flow in terminal_store_flow.items():
        store_flow[store] = store_flow.get(store, 0) + flow

    for store, flow in sorted(store_flow.items(), key=lambda x: x[1]):
        print(f"   {store}: {flow} од.")

    print("\n   Щоб збільшити постачання, підвищіть пропускну здатність маршрутів до цих магазинів.\n")

    print("4. Чи є вузькі місця, які можна усунути для підвищення ефективності мережі?")
    print("   Потенційні вузькі місця:")

    bottlenecks = []
    for u, v, data in G.edges(data=True):
        if 'capacity' in data and data['capacity'] < float('inf'):
            u_idx = node_mapping[u]
            v_idx = node_mapping[v]
            if flow_matrix[u_idx][v_idx] == data['capacity']:
                bottlenecks.append((u, v, data['capacity']))

    for u, v, capacity in bottlenecks:
        print(f"   {u} → {v}: {capacity} од. (використано на 100 %)")

    print("\n   Збільшення пропускної здатності цих маршрутів покращить загальний потік у мережі.")
def visualize_network(G, flow_matrix, node_mapping):
    G_vis = G.copy()

    for u, v, data in G.edges(data=True):
        if 'capacity' in data and data['capacity'] < float('inf'):
            u_idx = node_mapping[u]
            v_idx = node_mapping[v]
            flow = flow_matrix[u_idx][v_idx]
            G_vis[u][v]['flow'] = flow
            G_vis[u][v]['label'] = f"{flow}/{data['capacity']}"

    pos = {
        'Terminal 1': (-1, 1),
        'Terminal 2': (-1, -1),
        'Warehouse 1': (0, 1.5),
        'Warehouse 2': (0, 0.5),
        'Warehouse 3': (0, -0.5),
        'Warehouse 4': (0, -1.5),
    }

    store_positions = {}
    for i in range(1, 15):
        row = i - 1
        store_positions[f'Store {i}'] = (1, 1.5 - row * 0.5)

    pos.update(store_positions)

    plt.figure(figsize=(15, 10))

    node_colors = {
        'source': 'lightgreen',
        'sink': 'lightgreen',
        'terminal': 'lightblue',
        'warehouse': 'orange',
        'store': 'pink'
    }

    for node_type, color in node_colors.items():
        if node_type in ['source', 'sink']:
            continue
        nodes = [node for node in G_vis.nodes() if G_vis.nodes[node].get('type') == node_type]
        nx.draw_networkx_nodes(G_vis, pos, nodelist=nodes, node_color=color, node_size=500)

    for u, v, data in G_vis.edges(data=True):
        if u in ['source', 'sink'] or v in ['source', 'sink']:
            continue

        if 'flow' in data:
            width = 1 + data['flow'] * 0.1
            if data['flow'] > 0:
                nx.draw_networkx_edges(G_vis, pos, edgelist=[(u, v)], width=width, edge_color='blue')
            else:
                nx.draw_networkx_edges(G_vis, pos, edgelist=[(u, v)], width=1, edge_color='gray', style='dashed')
        else:
            nx.draw_networkx_edges(G_vis, pos, edgelist=[(u, v)], width=1, edge_color='gray')

    edge_labels = {(u, v): data.get('label', '') for u, v, data in G_vis.edges(data=True)
                  if 'label' in data and u not in ['source', 'sink'] and v not in ['source', 'sink']}
    nx.draw_networkx_edge_labels(G_vis, pos, edge_labels=edge_labels, font_size=8)

    nodes_to_label = [node for node in G_vis.nodes() if node not in ['source', 'sink']]
    nx.draw_networkx_labels(G_vis, pos, labels={n: n for n in nodes_to_label}, font_size=10)

    plt.title("Logistics Network Flow")
    plt.axis('off')
    plt.show()
