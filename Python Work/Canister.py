import logging


class Canister:
    #Capacity at 200  is only for testing purposes
    def __init__(self, contents, remaining=198, capacity=198):
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger("CANISTER")
        self.contents = contents
        self.capacity = capacity
        self.remaining = remaining

    def canDispense(self, units):
        if abs(self.remaining - units) <= 10:
            return False
        else:
            return True

    def dispense(self, units):
        self.remaining -= units

        if self.remaining < 0 and (units - self.remaining+units) > 10:
            self.remaining += units
            raise ValueError(self.contents + " is too empty to be dispensed.")

    def refill(self):
        self.remaining = self.capacity

    def status(self):
        self.log.info("Contents: " + self.contents +
                      " | Remaining Units: " + str(self.remaining))

    def getContents(self):
        return self.contents