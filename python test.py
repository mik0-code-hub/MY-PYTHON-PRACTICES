#%% THE SHOPPING CART AUDIT
store_stock = {
    'Laptop':   999.99,
    'Mouse':   24.99,
    'Keyboard':   49.99
}
customer_cart = ['Laptop', 'Mouse', 'HDMI_Cable', 'Keyboard']
def total_cost(items):
    total = 0
    for item in customer_cart:
        if item in store_stock:
            print(f"{item} is in Stock.")
            total += store_stock[item]
    return total
grand_total = total_cost(customer_cart)
print(f"The total cost of items in the Cart -> {grand_total}")

#%% SERVER ALERT REGISTRY
current_registry = {
    'CRITICAL':   3,
    'WARNING':   12,
    'INFO':   45
}
new_alerts = ['WARNING', 'INFO', 'UNKNOWN ERROR', 'CRITICAL', 'INFO']
def update_alerts(registry, alert_list):
    for alert in new_alerts:
        if alert in current_registry:
            current_registry[alert] += 1
    return current_registry