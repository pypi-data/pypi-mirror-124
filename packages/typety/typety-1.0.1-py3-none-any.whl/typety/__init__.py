# This is a typing effect
import time
import sys


def typingprint(text):
    """Types out a string of text
    
    Args:
        Print (str): What to type out"
        
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
        