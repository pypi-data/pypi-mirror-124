from datetime import datetime


class Colors:
    RESET = "\033[0m"

    class Foreground:
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"

    class ForegroundBright:
        BLACK = "\033[30;1m"
        RED = "\033[31;1m"
        GREEN = "\033[32;1m"
        YELLOW = "\033[33;1m"
        BLUE = "\033[34;1m"
        MAGENTA = "\033[35;1m"
        CYAN = "\033[36;1m"
        WHITE = "\033[37;1m"

    class Background:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        YELLOW = "\033[43m"
        BLUE = "\033[44m"
        MAGENTA = "\033[45m"
        CYAN = "\033[46m"
        WHITE = "\033[47m"

    class BackgroundBright:
        BLACK = "\033[40;1m"
        RED = "\033[41;1m"
        GREEN = "\033[42;1m"
        YELLOW = "\033[43;1m"
        BLUE = "\033[44;1m"
        MAGENTA = "\033[45;1m"
        CYAN = "\033[46;1m"
        WHITE = "\033[47;1m"

    class Formating:
        BOLD = "\033[1m"
        ITALIC = "\033[3m"
        UNDERLINE = "\033[4m"


class Logging:

    def getTimestamp(self):
        now = datetime.now()
        strTimestamp = now.strftime("%d-%m-%Y %H:%M:%S,%f")

        return f"{Colors.Formating.ITALIC}{strTimestamp}{Colors.RESET}"

    def info(self, text, timestamp=True, whole_line_colored=False, end="\n"):
        if not text:
            raise TypeError(
                "info() missing 1 required positional argument: 'text'")
            return

        if not timestamp:
            if not whole_line_colored:
                print(
                    f"{Colors.Foreground.GREEN}[ INFO ] {Colors.RESET}{text}{Colors.RESET}", end=end)
            else:
                print(
                    f"{Colors.ForegroundBright.GREEN}{Colors.Formating.BOLD}[ INFO ] {Colors.RESET}{Colors.Foreground.GREEN}{text}{Colors.RESET}", end=end)

        else:
            if not whole_line_colored:
                print(
                    f"{self.getTimestamp()} {Colors.Foreground.GREEN}[ INFO ] {Colors.RESET}{text}{Colors.RESET}", end=end)
            else:
                print(
                    f"{self.getTimestamp()} {Colors.ForegroundBright.GREEN}{Colors.Formating.BOLD}[ INFO ] {Colors.RESET}{Colors.Foreground.GREEN}{text}{Colors.RESET}", end=end)

    def warn(self, text, timestamp=True, whole_line_colored=False, end="\n"):
        if not text:
            raise TypeError(
                "warn() missing 1 required positional argument: 'text'")
            return

        if not timestamp:
            if not whole_line_colored:
                print(
                    f"{Colors.Foreground.YELLOW}[ WARN ] {Colors.RESET}{text}{Colors.RESET}", end=end)
            else:
                print(
                    f"{Colors.ForegroundBright.YELLOW}{Colors.Formating.BOLD}[ WARN ] {Colors.RESET}{Colors.Foreground.YELLOW}{text}{Colors.RESET}", end=end)

        else:
            if not whole_line_colored:
                print(
                    f"{self.getTimestamp()} {Colors.Foreground.YELLOW}[ WARN ] {Colors.RESET}{text}{Colors.RESET}", end=end)
            else:
                print(
                    f"{self.getTimestamp()} {Colors.ForegroundBright.YELLOW}{Colors.Formating.BOLD}[ WARN ] {Colors.RESET}{Colors.Foreground.YELLOW}{text}{Colors.RESET}", end=end)

    def fail(self, text, timestamp=True, whole_line_colored=False, end="\n"):
        if not text:
            raise TypeError(
                "fail() missing 1 required positional argument: 'text'")
            return

        if not timestamp:
            if not whole_line_colored:
                print(
                    f"{Colors.Foreground.RED}[ FAIL ] {Colors.RESET}{text}{Colors.RESET}", end=end)
            else:
                print(
                    f"{Colors.ForegroundBright.RED}{Colors.Formating.BOLD}[ FAIL ] {Colors.RESET}{Colors.Foreground.RED}{text}{Colors.RESET}", end=end)

        else:
            if not whole_line_colored:
                print(
                    f"{self.getTimestamp()} {Colors.Foreground.RED}[ FAIL ] {Colors.RESET}{text}{Colors.RESET}", end=end)
            else:
                print(
                    f"{self.getTimestamp()} {Colors.ForegroundBright.RED}{Colors.Formating.BOLD}[ FAIL ] {Colors.RESET}{Colors.Foreground.RED}{text}{Colors.RESET}", end=end)

    def infoLoad(self, text, timestamp=True, end="\n"):
        if not text:
            raise TypeError(
                "infoLoad() missing 1 required positional argument: 'text'")
            return

        if not timestamp:
            print(
                f"{Colors.ForegroundBright.GREEN}[ INFO ] {Colors.RESET}{Colors.Foreground.CYAN}{text}{Colors.RESET}", end=end)

        else:
            print(
                f"{self.getTimestamp()} {Colors.ForegroundBright.GREEN}[ INFO ] {Colors.RESET}{Colors.Foreground.CYAN}{text}{Colors.RESET}", end=end)


class Header:
    def createHeader(self, text, bold=False, italic=False, underline=False):
        if not text:
            raise TypeError(
                "createHeader() missing 1 required positional argument: 'text'")
            return
        
        if bold:
            if italic:
                if underline:
                    print(
                        f"{Colors.Foreground.MAGENTA}{Colors.Formating.BOLD}{Colors.Formating.ITALIC}{Colors.Formating.UNDERLINE}{text}{Colors.RESET}")
                else:
                    print(
                        f"{Colors.Foreground.MAGENTA}{Colors.Formating.BOLD}{Colors.Formating.ITALIC}{text}{Colors.RESET}")

            else:
                if underline:
                    print(
                        f"{Colors.Foreground.MAGENTA}{Colors.Formating.BOLD}{Colors.Formating.UNDERLINE}{text}{Colors.RESET}")
                else:
                    print(
                        f"{Colors.Foreground.MAGENTA}{Colors.Formating.BOLD}{text}{Colors.RESET}")

        else:
            if italic:
                if underline:
                    print(
                        f"{Colors.Foreground.MAGENTA}{Colors.Formating.ITALIC}{Colors.Formating.UNDERLINE}{text}{Colors.RESET}")
                else:
                    print(
                        f"{Colors.Foreground.MAGENTA}{Colors.Formating.ITALIC}{text}{Colors.RESET}")

            else:
                if underline:
                    print(
                        f"{Colors.Foreground.MAGENTA}{Colors.Formating.UNDERLINE}{text}{Colors.RESET}")
                else:
                    print(
                        f"{Colors.Foreground.MAGENTA}{text}{Colors.RESET}")

