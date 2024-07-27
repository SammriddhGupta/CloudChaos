import sys
import os

# This is necessary for pytest to find the modules to be tested,
# as pytest does not automatically add the parent directory to the path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
