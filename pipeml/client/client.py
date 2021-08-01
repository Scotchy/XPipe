
from .session import Session

def connect(url):
    """Connect to a pipeml server

    Args:
        url (str): URL of the server hosting the pipeml API

    Returns:
        session (Session): A session
    """
    return Session(url)
