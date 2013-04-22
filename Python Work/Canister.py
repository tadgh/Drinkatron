

class Canister:
    #Capacity at 200  is only for testing purposes
    def __init__(self, contents, remaining = 200, capacity=200):
        self.contents = contents
        self.capacity = capacity
        self.remaining = remaining
        pumpTime =