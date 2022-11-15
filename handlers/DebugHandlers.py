from pprint import pprint
import os

try:
    DEBUG = os.environ["DEBUG"] == "TRUE"
except KeyError:
    DEBUG = False
def print_debug(*args, **kwargs):
    if DEBUG:
        print("[DEBUG] ", end="")
        print(*args, **kwargs)

def pprint_debug(*args, **kwargs):
    if DEBUG:
        print("[DEBUG]:")
        pprint(*args, **kwargs)