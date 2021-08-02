from .Aggregator import Aggregator
from .ProgramExecutor import ProgramExecutor

class AnalyticsServer():
    def __init__(self, public_key):
        self.aggregator = Aggregator(public_key)
        self.program_executor = ProgramExecutor(public_key)

    # Once data is aggregated and encrypted, we need to propagate this to the ProgramExecutor
        # TODO: Is there a nicer way to store encrypted data and the public key in AS, because currently we are storing the public key and encrypted data in both Aggregator + ProgramExecutor, and if one updates the other needs to as well
    def init_executor(self):
        self.program_executor = ProgramExecutor(self.aggregator.public_key, self.aggregator.data_encrypted)

    def __str__(self):
        return "AnalyticsServer" + str({"Aggregator": self.aggregator.__str__(), "ProgramExecutor": self.program_executor.__str__()})
