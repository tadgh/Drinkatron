import logging


class Canister:
    #Capacity at 200  is only for testing purposes
    def __init__(self, contents, remaining=946, capacity=946):
        logging.basicConfig(file="C:\\runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("CANISTER")
        self.contents = contents
        self.capacity = capacity
        self.remaining = remaining

    def dispense(self, units):
        self.remaining -= units

        if self.remaining < 0 and (units - self.remaining+units) > 10:
            self.remaining += units
            raise ValueError(self.contents + "is too empty to be \
                                                dispensed.")

    def refill(self):
        pass

    def status(self):
        self.log.info("Contents: " + self.contents +
                      "\nRemaining Units: " + str(self.remaining))


