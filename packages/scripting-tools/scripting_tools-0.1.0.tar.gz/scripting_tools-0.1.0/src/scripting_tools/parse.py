from .argsguard import args_guard

def parse_int(string:str) -> int:
    """
    A function to parse string characters into int
    -> string: str => a string of chars, ex : "abc12a3"
    ----
    => int: numbers present inside the string passed in, ex : 123
    """

    if not isinstance(string, str):
        raise TypeError('string must be a string')

    return int("".join([i for i in string.strip() if i.isnumeric()]))

def parse_float(string:str) -> float:
    """
    A function to parse string characters into float
    -> string: str => a string of chars, ex : "abc12a.a3"
    ----
    => float: numbers present inside the string passed in, ex : 12.3
    """

    if not isinstance(string, str):
        raise TypeError('string must be a string')

    return float("".join([i for i in string.strip() if i.isnumeric() or i == "."]))