from .colorama_ext import Fore, Style
from . import ostools
from datetime import datetime
from time import time

class log:
    def __init__(self, file_location:str, prefix:str, print_to_console:bool=True, append:bool=False, warnings_enabled=True, date_time_displayed:bool=False, time_since_start:bool=True, datetime_format:str="%H:%M:%S", updates_save=False) -> None:
        """
        A function to initialise the log class, which will log given updates to a certain file.
        -> file_location*: str => This takes in the file in which logs will be stored.
        -> prefix*: str => This will be printed out in the begining of the file with all system information which will be printed by default.
        -> print_to_console => This will print to console everytime something is logged.
        -> append: bool (False) => This will append to the given file instead of overwriting the file by default.
        -> warnings_enabled: bool (True) => This will save logs which are marked as "WARNING".
        -> date_time_displayed: bool (False) => This will display a datetime stamp everytime something is logged.
        -> time_since_start: bool (True) => This will display a timestamp (seconds since logging has started) everytime something is logged.
        -> datetime_format: str ("%H:%M:%S") => If 'date_time_displayed' is enabled, the logger will use this given datetime format. (datetime module)
        -> updates_save: bool (False) => WARNING; This will slow down the program if enabled. This will immediately save all updates everytime when something is logged.
        """

        self.PRINT_TO_CONSOLE = print_to_console
        self.APPEND = append
        self.FILE_LOCATION = file_location
        self.PREFIX = prefix
        self.WARNINGS_ENABLED = warnings_enabled
        self.DATE_TIME_DISPLAYED = date_time_displayed
        self.TIME_SINCE_START = time_since_start
        self.DATETIME_FORMAT = datetime_format
        self.UPDATES_SAVE = updates_save

        self.log_content = ""

        self.start_time = 0
        self.has_started = False

    def start(self) -> None:
        """
        Starts the logging process.
        ----
        => None
        """
        print(f"{Fore.GREEN}Logging has started.{Fore.RESET}")
        self.start_time = time()
        self.has_started = True
        file_content = f"{self.PREFIX}\n[{ostools.OS} - {datetime.now()}]\n\n"
        if self.APPEND:
            with open(self.FILE_LOCATION, "a") as log_file:
                log_file.write(file_content)
        else:
            with open(self.FILE_LOCATION, "w") as log_file:
                log_file.write(file_content)

    def log(self, message:str) -> None:
        """
        Logs a message to the log file. (Generic)
        -> message: str => The message to be logged.
        ----
        => None
        """
        if not self.has_started:
            self.start()

        content = ""

        if self.DATE_TIME_DISPLAYED:
            content = f"[{datetime.now().strftime(self.DATETIME_FORMAT)}] "

        if self.TIME_SINCE_START:
            content += f"[{int(time() - self.start_time)}] {message}"

        if self.PRINT_TO_CONSOLE:
            print(content)

        if self.UPDATES_SAVE:
            with open(self.FILE_LOCATION, "a") as log_file:
                log_file.write(content + "\n")
        else:
            self.log_content += content + "\n"

    def warning(self, message:str) -> None:
        """
        Logs a warning to the log file.
        -> message: str => The message to be logged.
        ----
        => None
        """
        if not self.has_started:
            self.start()

        if self.WARNINGS_ENABLED:
            content = ""

            if self.DATE_TIME_DISPLAYED:
                content = f"[{datetime.now().strftime(self.DATETIME_FORMAT)}] "

            if self.TIME_SINCE_START:
                content += f"[{int(time() - self.start_time)}] WARNING : {message}"

            if self.PRINT_TO_CONSOLE:
                if self.WARNINGS_ENABLED:
                    print(f"{Fore.YELLOW}{content}{Fore.RESET}")
                else:
                    print(f"{Fore.LIGHTBLACK_EX}{Style.DIM}Warnings disabled.{Style.RESET_ALL}")

            if self.UPDATES_SAVE:
                with open(self.FILE_LOCATION, "a") as log_file:
                    log_file.write(content + "\n")
            else:
                self.log_content += content + "\n"

    def info(self, message:str) -> None:
        """
        Logs an info to the log file.
        -> message: str => The message to be logged.
        ----
        => None
        """
        if not self.has_started:
            self.start()

        content = ""

        if self.DATE_TIME_DISPLAYED:
            content = f"[{datetime.now().strftime(self.DATETIME_FORMAT)}] "

        if self.TIME_SINCE_START:
            content += f"[{int(time() - self.start_time)}] INFO : {message}"

        if self.PRINT_TO_CONSOLE:
            print(f"{Fore.CYAN}{content}{Fore.RESET}")

        if self.UPDATES_SAVE:
            with open(self.FILE_LOCATION, "a") as log_file:
                log_file.write(content + "\n")
        else:
            self.log_content += content + "\n"

    def success(self, message:str) -> None:
        """
        Logs a success to the log file.
        -> message: str => The message to be logged.
        ----
        => None
        """
        if not self.has_started:
            self.start()

        content = ""

        if self.DATE_TIME_DISPLAYED:
            content = f"[{datetime.now().strftime(self.DATETIME_FORMAT)}] "

        if self.TIME_SINCE_START:
            content += f"[{int(time() - self.start_time)}] SUCCESS : {message}"

        if self.PRINT_TO_CONSOLE:
            print(f"{Fore.GREEN}{content}{Fore.RESET}")

        if self.UPDATES_SAVE:
            with open(self.FILE_LOCATION, "a") as log_file:
                log_file.write(content + "\n")
        else:
            self.log_content += content + "\n"

    def error(self, message:str) -> None:
        """
        Logs an error to the log file.
        -> message: str => The message to be logged.
        ----
        => None
        """
        if not self.has_started:
            self.start()

        content = ""

        if self.DATE_TIME_DISPLAYED:
            content = f"[{datetime.now().strftime(self.DATETIME_FORMAT)}] "

        if self.TIME_SINCE_START:
            content += f"[{int(time() - self.start_time)}] ERROR : {message}"

        if self.PRINT_TO_CONSOLE:
            print(f"{Fore.RED}{content}{Fore.RESET}")

        if self.UPDATES_SAVE:
            with open(self.FILE_LOCATION, "a") as log_file:
                log_file.write(content + "\n")
        else:
            self.log_content += content + "\n"

    def end(self) -> None:
        """
        Ends the logging process.
        ----
        => None
        """
        if not self.UPDATES_SAVE:
            with open(self.FILE_LOCATION, "a") as log_file:
                log_file.write(self.log_content + "\n\n")

        print(f"{Fore.GREEN}Logging has ended.{Fore.RESET}")
