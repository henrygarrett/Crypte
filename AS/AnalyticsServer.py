from .Aggregator import Aggregator
from .ProgramExecutor import ProgramExecutor

class AnalyticsServer():
    def __init__(self):
        self.aggregator = Aggregator()
        self.program_executor = ProgramExecutor()
        self.init_executor()

    def init_executor(self):
        self.program_executor = ProgramExecutor(self.aggregator.data_encrypted)

    def __str__(self):
        return "AnalyticsServer" + str({"Aggregator": self.aggregator.__str__(), "ProgramExecutor": self.program_executor.__str__()})
