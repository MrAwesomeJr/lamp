import datetime


class Update:
    def __init__(self, timestamp, color):
        # timestamp should be of type datetime.timedelta()
        self.timestamp = timestamp
        # color should be a list of 50 tuples, each tuple containing 3 ints, each int between 0-255.
        self.color = color
