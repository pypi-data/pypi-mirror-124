import random
import string

def random_string(length:int, letters:bool=True, numbers:bool=False, symbols:bool=False):
    """
    Generates a random string of a given length.
    -> length*: int => The length of the string to be generated.
    -> letters: bool (True) => Whether to include letters.
    -> numbers: bool (False) => Whether to include numbers.
    -> symbols: bool (False) => Whether to include symbols.
    ----
    => The generated string.
    """

    content = ""

    if letters:
        content += string.ascii_letters

    if numbers:
        content += string.digits
        
    if symbols:
        content += string.punctuation
    
    return ''.join(random.choice(content) for _ in range(length))
