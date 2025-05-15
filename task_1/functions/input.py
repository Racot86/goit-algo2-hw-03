import networkx as nx


def create_logistics_network():
    G = nx.DiGraph()

    G.add_node('source', type='source')
    G.add_node('sink', type='sink')

    G.add_node('Terminal 1', type='terminal')
    G.add_node('Terminal 2', type='terminal')

    for i in range(1, 5):
        G.add_node(f'Warehouse {i}', type='warehouse')

    for i in range(1, 15):
        G.add_node(f'Store {i}', type='store')

    G.add_edge('source', 'Terminal 1', capacity=float('inf'))
    G.add_edge('source', 'Terminal 2', capacity=float('inf'))

    for i in range(1, 15):
        G.add_edge(f'Store {i}', 'sink', capacity=float('inf'))

    terminal_to_warehouse = [
        ('Terminal 1', 'Warehouse 1', 25),
        ('Terminal 1', 'Warehouse 2', 20),
        ('Terminal 1', 'Warehouse 3', 15),
        ('Terminal 2', 'Warehouse 3', 15),
        ('Terminal 2', 'Warehouse 4', 30),
        ('Terminal 2', 'Warehouse 2', 10),
    ]

    for source, target, capacity in terminal_to_warehouse:
        G.add_edge(source, target, capacity=capacity)

    warehouse_to_store = [
        ('Warehouse 1', 'Store 1', 15),
        ('Warehouse 1', 'Store 2', 10),
        ('Warehouse 1', 'Store 3', 20),
        ('Warehouse 2', 'Store 4', 15),
        ('Warehouse 2', 'Store 5', 10),
        ('Warehouse 2', 'Store 6', 25),
        ('Warehouse 3', 'Store 7', 20),
        ('Warehouse 3', 'Store 8', 15),
        ('Warehouse 3', 'Store 9', 10),
        ('Warehouse 4', 'Store 10', 20),
        ('Warehouse 4', 'Store 11', 10),
        ('Warehouse 4', 'Store 12', 15),
        ('Warehouse 4', 'Store 13', 5),
        ('Warehouse 4', 'Store 14', 10),
    ]

    for source, target, capacity in warehouse_to_store:
        G.add_edge(source, target, capacity=capacity)

    return G
