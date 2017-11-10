class ParameterException(Exception):
    def __init__(self, message=None):
        if message is not None:
            self.message = message
        else:
            self.message = "Invalid parameters."
