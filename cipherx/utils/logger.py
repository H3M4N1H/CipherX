from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

ARROW = "→"  # kept out of f-strings for Python 3.9 compatibility


class Logger:
    def __init__(self):
        pass

    def info(self, msg):
        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {msg}")

    def success(self, msg):
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {msg}")

    def warning(self, msg):
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {msg}")

    def error(self, msg):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} {msg}")

    def section(self, msg):
        print(f"\n{Fore.MAGENTA}{'='*10} {msg} {'='*10}{Style.RESET_ALL}")

    def layer(self, num, method, result):
        truncated = result[:60] + ("..." if len(result) > 60 else "")
        print(
            f"{Fore.BLUE}[Layer {num}]{Style.RESET_ALL} "
            f"{Fore.YELLOW}{method:<15}{Style.RESET_ALL} {ARROW} {truncated}"
        )

    def flag(self, result):
        print(f"\n{Fore.GREEN}{'#'*20} FLAG FOUND {'#'*20}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'#'*52}{Style.RESET_ALL}\n")

    def chain(self, chain_list):
        if not chain_list:
            print(f"{Fore.YELLOW}[Chain]{Style.RESET_ALL} No layers decoded")
            return
        joined = f" {ARROW} ".join(chain_list)
        print(f"{Fore.CYAN}[Chain]{Style.RESET_ALL} {joined}")
