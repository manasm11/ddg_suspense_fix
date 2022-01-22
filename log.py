def p(*args, **kwargs):
    print(*args, **kwargs, flush=True)

def error(msg, *args, **kwargs):
    p("[ERROR]:", msg, *args, **kwargs)
    exit(1)

def info(msg, *args, **kwargs):
    p("[INFO]:", msg, *args, **kwargs)