from pprint import pprint


DEBUG = True
def print_debug(*args, **kwargs):
    if DEBUG:
        print("[DEBUG] ", end="")
        print(*args, **kwargs)

def pprint_debug(*args, **kwargs):
    if DEBUG:
        print("[DEBUG]:")
        pprint(*args, **kwargs)