import random

# Simulation parameters
SIM_DAYS = 30         # Number of days to simulate
INITIAL_STOCK = 100   # Starting inventory
REORDER_POINT = 20    # When to reorder
ORDER_QUANTITY = 50   # Restock amount
LEAD_TIME = 2         # Days before restock arrives
MAX_DEMAND = 10       # Maximum daily demand

class InventorySystem:
    def __init__(self, initial_stock):
        self.stock = initial_stock
        self.pending_orders = []
        self.daily_demand = []
        self.stockouts = 0
        self.total_orders = 0

    def place_order(self):
        self.pending_orders.append(LEAD_TIME)
        self.total_orders += 1

    def receive_order(self):
        self.stock += ORDER_QUANTITY

    def daily_update(self):
        # Reduce lead time for pending orders
        self.pending_orders = [days - 1 for days in self.pending_orders if days > 1]
        if LEAD_TIME in self.pending_orders:
            self.receive_order()
            self.pending_orders.remove(LEAD_TIME)

        # Simulate daily demand
        demand = random.randint(0, MAX_DEMAND)
        self.daily_demand.append(demand)

        if demand > self.stock:
            self.stockouts += 1
            self.stock = 0
        else:
            self.stock -= demand

        # Check if a new order is needed
        if self.stock <= REORDER_POINT and LEAD_TIME not in self.pending_orders:
            self.place_order()

# Run simulation
inventory = InventorySystem(INITIAL_STOCK)

for day in range(SIM_DAYS):
    inventory.daily_update()

# Display results
print(f"Final stock level: {inventory.stock}")
print(f"Total orders placed: {inventory.total_orders}")
print(f"Stockouts occurred: {inventory.stockouts} times")
