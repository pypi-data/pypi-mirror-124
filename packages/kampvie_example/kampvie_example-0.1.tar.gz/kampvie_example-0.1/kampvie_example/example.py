import platform

current = platform.uname()

def get_release():
    return current.release