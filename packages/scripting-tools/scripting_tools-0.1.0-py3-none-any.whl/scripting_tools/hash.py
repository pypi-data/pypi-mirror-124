from hashlib import sha256
from uuid import uuid4
from .argsguard import args_guard

def hash(text: str) -> str:
    """
    Hashes a given text using the well known sha256 algorithm
    -> text: str = The string to be hashed
    ----
    => str: the hashed string
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    salt = uuid4().hex
    return sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt

def validate_hash(hashed_text: str, check_text: str):
    """
    Checks if a given text matches a hashed(using sha256) text
    -> hashed_text: str = The hashed text
    -> check_text: str = The text which is to be checked with the hashed text
    ----
    => bool: Boolean value of : if the check_text matches hashed_text
    """

    if not isinstance(hashed_text, str):
        raise TypeError("hashed_text must be a string")

    if not isinstance(check_text, str):
        raise TypeError("check_text must be a string")

    try:
        text, salt = hashed_text.split(':')
        return text == sha256(salt.encode() + check_text.encode()).hexdigest()
    except Exception:
        return False