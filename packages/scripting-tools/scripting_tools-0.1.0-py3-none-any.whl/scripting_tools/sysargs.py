import sys

SYSTEM_ARGUMENTS = sys.argv[1:]

def args_to_dictionary(default_msg:str = "", boolean_options:list=[], arguments:list=SYSTEM_ARGUMENTS) -> dict:
    """
    A function that returns a dictionary of the system arguments passed to the program.
    -> default_msg: str => A default message to be displayed when the program is called without any arguments.
    -> boolean_options: list of boolean options which will take no arguments.
    -> arguments: list of arguments to passed to the program. (defaults to sys.argv).
    ----
    => dict: A dictionary of the system arguments passed to the program.
    """
    system_args = arguments
    option = True
    options_list = []
    arguments_list = []

    if (not isinstance(boolean_options, list)):
        raise ValueError('boolean options must be a list')
    
    if (not isinstance(default_msg, str)):
        raise ValueError('default_msg must be a string')

    if not system_args:
        print(default_msg)
    else:
        for i in system_args:
            if option and i.startswith("-"):
                options_list.append(i)
                if i not in boolean_options:
                    option = False
                else:
                    arguments_list.append(True)

            elif not option:
                arguments_list.append(i)
                option = True
            else:
                raise ValueError('An option that starts with "-", must be specified')

    if not option:
        raise ValueError(f"An argument to option {system_args[-1]}, must be specified")

    return dict(zip(options_list, arguments_list))

#print(sys.argv)
