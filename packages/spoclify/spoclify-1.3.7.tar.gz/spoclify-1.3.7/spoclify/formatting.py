from ansi.color import fg, fx

PRINT_LEVELS = {"fatal": fg.red, "warning": fg.yellow, "info": fg.white, "attention": fg.green}

def fprint(text, level=""):
    print(PRINT_LEVELS.get(level.lower(), lambda x: x)(text) + str(fx.reset))

def info(text): fprint(text, "info")

def warning(text): fprint(text, "warning")

def fatal(text): fprint(text, "fatal")

def attention(text): fprint(text, "attention")