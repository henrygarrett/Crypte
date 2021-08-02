from .Aggregator import Aggregator
from .ProgramExecutor import ProgramExecutor

class AnalyticsServer():
    def __init__(self, public_key):
        self.aggregator = Aggregator(public_key)
        self.program_executor = ProgramExecutor(public_key, len(self.aggregator.data), len(self.aggregator.data[0]))

    def __str__(self):
        return "AnalyticsServer" + str({"Aggregator": self.aggregator.__str__(), "ProgramExecutor": self.program_executor.__str__()})
