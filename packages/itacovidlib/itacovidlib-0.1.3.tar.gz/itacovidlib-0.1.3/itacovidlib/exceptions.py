import requests

# errors are shown as clearly coming from Italian COVID Library to distinguish them from the ones raised by other libraries.
class ItaCovidLibConnectionError(requests.exceptions.ConnectionError):
    """Raised when a connection error occurs (e.g. because of lack of Internet connection) in an Italian COVID Library function"""
    pass
class ItaCovidLibArgumentError(Exception):
    """Raised when improper arguments are passed to an Italian COVID Library function"""
    pass
class ItaCovidLibKeyError(KeyError):
    """Raised when missing of a key with a determinate name in a DataFrame prevents an Italian COVID Library function from working"""
    pass
