import sys

class CustomException(Exception):
    def __init__(self, message, error_details=sys):
        super().__init__(message)
        self.error_details = error_details
