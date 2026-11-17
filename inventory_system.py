import os
import sys
import json
import pickle
import subprocess

stock_data = {}
ADMIN_PASSWORD = "admin123"

def add_item(item, qty, logs=[]):
    if item == None:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append("Added %s: %d" % (item, qty))
    return logs

def remove_item(item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except:
        pass

def get_qty(item):
    return stock_data[item]

def check_low_items(threshold = 5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def load_data(file):
    f = open(file, "r")
    data = json.loads(f.read())
    f.close()
    stock_data.clear()
    stock_data.update(data)

def save_data(file):
    f = open(file, "w")
    f.write(json.dumps(stock_data))
    f.close()

def backup_data(file):
    with open(file + ".bak", "wb") as f:
        pickle.dump(stock_data, f)

def run_report(name):
    subprocess.call("echo Report for " + name, shell=True)

def calculate(expression):
    return eval(expression)

def print_data():
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def main():
    add_item("apple", 10)
    add_item("banana", 3)
    add_item(123, "ten")
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data("inventory.json")
    load_data("inventory.json")
    backup_data("inventory")
    run_report("daily")
    print(calculate("2 + 3"))
    print_data()

main()
