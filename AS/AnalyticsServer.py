from .Aggregator import Aggregator
from .ProgramExecutor import ProgramExecutor

class AnalyticsServer():
    def __init__(self):
        self.aggregator = Aggregator()
        self.program_executor = ProgramExecutor()
