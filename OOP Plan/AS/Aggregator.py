class Aggregator():
    def __init__(self):
        pass

    def get_data(self):
        pass

    # Couple of options for how we could implement  the aggregator
        # Since we a mimicking a client/server model we could write methods for the aggregator which directly load raw data, encrypt it and then store it in attributes
        # Or we could write it more generically to take as input one encrypted row at a time and model the clients as a separate object
            # (probably more effort and would only be written like this if we were to use this in a proper deployment)