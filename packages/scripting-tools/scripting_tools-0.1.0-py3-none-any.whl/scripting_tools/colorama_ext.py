from colorama import init, Fore, Back, Style

init(convert=True)

def info(message):
    return f"{Fore.CYAN}{message}{Fore.RESET}"

def success(message):
    return f"{Fore.GREEN}{message}{Fore.RESET}"

def warning(message):
    return f"{Fore.YELLOW}{message}{Fore.RESET}"

def error(message):
    return f"{Fore.RED}{message}{Fore.RESET}"

def debug(message):
    return f"{Fore.MAGENTA}{message}{Fore.RESET}"

def disabled(message):
    return f"{Fore.LIGHTBLACK_EX}{Style.DIM}{message}{Style.RESET_ALL}"