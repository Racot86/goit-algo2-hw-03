
import csv
import timeit
from BTrees.OOBTree import OOBTree


def add_item_to_tree(tree, price_tree, item):
    tree[item['ID']] = item

    price = float(item['Price'])
    if price not in price_tree:
        price_tree[price] = []
    price_tree[price].append(item)

def add_item_to_dict(dictionary, item):
    dictionary[item['ID']] = item

def range_query_tree(price_tree, min_price, max_price):
    result = []
    for price, items_list in price_tree.items(min_price, max_price):
        result.extend(items_list)
    return result

def range_query_dict(dictionary, min_price, max_price):
    result = []
    for _, item in dictionary.items():
        if min_price <= float(item['Price']) <= max_price:
            result.append(item)
    return result

def load_data(file_path):
    items = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row)
    return items

def main():
    file_path = 'generated_items_data.csv'
    items = load_data(file_path)

    tree = OOBTree()
    price_tree = OOBTree()
    dictionary = {}

    for item in items:
        add_item_to_tree(tree, price_tree, item)
        add_item_to_dict(dictionary, item)

    min_price = 100
    max_price = 500

    tree_time = timeit.timeit(
        lambda: range_query_tree(price_tree, min_price, max_price),
        number=100
    )

    dict_time = timeit.timeit(
        lambda: range_query_dict(dictionary, min_price, max_price),
        number=100
    )

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if __name__ == '__main__':
    main()
