from .Aggregator import  Aggregator

class AnalyticsServer():
    def __init__(self):
        self.aggregator = Aggregator()
        pass

    # Operators

        # NOTE: If the operators are particularly long
            # then it may be beneficial to create a ProgramExecutor class and to store that as an attribute inside AS (like we do for PrivacyEngine/KeyManager in CSP)

     # args is a placeholder for whatever arguments are needed
    def project(self, args):
        self.aggregator.get_data() # Can use aggregator object as a way to manage the encrypted table of all the data
        pass

    def cross_product(self, args):
        pass

    def filter(self, args):
        pass

    # etc...