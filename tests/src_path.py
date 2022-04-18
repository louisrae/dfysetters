"""This mini module imports the path to the parent directory to call modules 
from. It is a bit of a hack, but it is the only way I could get pytest, the 
file and the test file to all work together"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]) + "/dfysetters")
