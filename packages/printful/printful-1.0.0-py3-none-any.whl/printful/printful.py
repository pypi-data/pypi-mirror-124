import time
import os
import colorama

from colorama import Fore

colorama.init()

# getters
def get_time():
    return time.strftime("%H:%M:%S")

# main
class bprint():
    # default
    def success(message):
        print(f"[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.LIGHTGREEN_EX}success{Fore.RESET}] {message}")

    def error(message):
        print(f"[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.LIGHTRED_EX}error{Fore.RESET}] {message}")

    def info(message):
        print(f"[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.YELLOW}info{Fore.RESET}] {message}")

    # speical
    def input(message):
        print(f"[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.BLUE}input{Fore.RESET}] {message}: ", end='')
        item = str(input(''))
        return item

    def pause():
        print(f"[{Fore.LIGHTBLACK_EX}{get_time()}{Fore.RESET}] [{Fore.BLUE}pause{Fore.RESET}] Press any key.")
        os.system('pause >nul')