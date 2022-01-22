def p(*args, **kwargs):
    print(*args, **kwargs, flush=True)

def exception(msg, *args, **kwargs):
    p("[ERROR]:", msg, *args, **kwargs)
    p("Stopping the execution...")
    exit(1)

def error(msg, *args, **kwargs):
    p("[ERROR]:", msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    p("[INFO]:", msg, *args, **kwargs)