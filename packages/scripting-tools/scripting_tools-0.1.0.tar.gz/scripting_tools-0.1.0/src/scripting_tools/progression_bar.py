
def progress_bar (iteration, total, prefix = ' ', suffix = ' ', decimals = 1, length = 100, fill = '█', printEnd = "\r") -> None:
    """
    Call in a loop to create terminal progress bar
    -> iteration*: int => current iteration
    -> total*: int => total iterations
    -> prefix: str => prefix string
    -> suffix: str => suffix string
    -> decimals: int => positive number of decimals in percent complete
    -> length: int => character length of bar
    -> fill: str => bar fill character
    -> printEnd: str => end character (e.g. "\r", "\r\n")
    ----
    => None
    """

    if not isinstance(iteration, int):
        raise ValueError("iteration must be an integer")

    if not isinstance(total, int):
        raise ValueError("total must be an integer")    

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()