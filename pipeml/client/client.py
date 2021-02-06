
from .session import Session

def connect(url):
    return Session(url)
