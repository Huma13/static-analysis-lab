"""Simple inventory management system used for the static analysis lab."""

import ast
import json
import operator
import os

stock_data = {}
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def add_item(item, qty, logs=None):
    """Add qty units of item to stock and record the action in logs."""
    if logs is None:
        logs = []
    if not isinstance(item, str) or not isinstance(qty, int):
        raise ValueError(f"Invalid item or quantity: {item!r}, {qty!r}")
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"Added {item}: {qty}")
    return logs


def remove_item(item, qty):
    """Remove qty units of item; delete the item if stock reaches zero."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print("Cannot remove missing item:", item)


def get_qty(item):
    """Return the stock quantity of item."""
    return stock_data[item]


def check_low_items(threshold=5):
    """Return items whose stock is below threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def load_data(file):
    """Load stock data from a JSON file."""
    with open(file, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    stock_data.clear()
    stock_data.update(data)


def save_data(file):
    """Save stock data to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(stock_data, handle)


def backup_data(file):
    """Write a JSON backup of the stock data."""
    with open(file + ".bak", "w", encoding="utf-8") as handle:
        json.dump(stock_data, handle)


def run_report(name):
    """Print a report header for the given report name."""
    print("Report for " + name)


def evaluate(node):
    """Safely evaluate a parsed arithmetic expression."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](
            evaluate(node.left), evaluate(node.right))
    raise ValueError("Unsupported expression")


def calculate(expression):
    """Calculate a simple arithmetic expression without using eval."""
    return evaluate(ast.parse(expression, mode="eval").body)


def print_data():
    """Print every item and its quantity."""
    print("Items Report")
    for item, qty in stock_data.items():
        print(item, "->", qty)


def main():
    """Run a demo of the inventory system."""
    add_item("apple", 10)
    add_item("banana", 3)
    try:
        add_item(123, "ten")
    except ValueError as error:
        print("Skipped invalid entry:", error)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data("inventory.json")
    load_data("inventory.json")
    backup_data("inventory")
    run_report("daily")
    print(calculate("2 + 3"))
    print_data()


if __name__ == "__main__":
    main()
