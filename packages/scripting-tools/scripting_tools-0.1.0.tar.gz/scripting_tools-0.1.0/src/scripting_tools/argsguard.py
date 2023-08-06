from functools import wraps
from inspect import isclass
from types import UnionType

def args_guard(*types):
    """A function decorator to static/type check the positional arguments passed into a function.
    -> *types: type = A bunch of types/classes which will be type checked with a function while calling it.
    ----
    => returns decorator_guard: function
    """
    def decorator_guard(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(len(types)):
                if isclass(types[i]) or isinstance(types[i], UnionType):
                    if not isinstance(args[i], types[i]):
                        raise ValueError(f"{args[i]!r} is not a type of '{types[i]}'")
                else:
                    print(type(types[i]))
                    raise ValueError(f"{types[i]!r} is not a class/object")

            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_guard