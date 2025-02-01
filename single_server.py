import random
import simpy

# Simulation parameters
RANDOM_SEED = 42
ARRIVAL_RATE = 1.5  # Customers per minute (Poisson)
SERVICE_RATE = 2.0   # Service rate (Exponential)
SIM_TIME = 100       # Simulation time in minutes

class SingleServerQueue:
    def __init__(self, env):
        self.env = env
        self.server = simpy.Resource(env, capacity=1)
        self.total_wait_time = 0
        self.customer_count = 0

    def serve_customer(self, customer):
        service_time = random.expovariate(SERVICE_RATE)
        yield self.env.timeout(service_time)
        self.total_wait_time += self.env.now
        self.customer_count += 1

def customer_generator(env, queue):
    customer_id = 0
    while True:
        interarrival_time = random.expovariate(ARRIVAL_RATE)
        yield env.timeout(interarrival_time)
        customer_id += 1
        env.process(handle_customer(env, queue, customer_id))

def handle_customer(env, queue, customer_id):
    arrival_time = env.now
    with queue.server.request() as request:
        yield request
        wait_time = env.now - arrival_time
        queue.total_wait_time += wait_time
        yield env.process(queue.serve_customer(customer_id))

# Run the simulation
random.seed(RANDOM_SEED)
env = simpy.Environment()
queue = SingleServerQueue(env)
env.process(customer_generator(env, queue))
env.run(until=SIM_TIME)

# Results
average_wait_time = queue.total_wait_time / max(queue.customer_count, 1)
print(f"Total customers served: {queue.customer_count}")
print(f"Average waiting time: {average_wait_time:.4f} minutes")
