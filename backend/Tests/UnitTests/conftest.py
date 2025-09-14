import sys
from pathlib import Path

# Add the 'backend' folder to the sys path
# since this file is in Flare/backend/Tests/UnitTests/, 
# we need to go two folders up to get the path to the backend folder
backend_dir = Path(__file__).resolve().parents[2]
#we insert that path on the front so the python interpreter finds it faster (yeah, yeah, a little tacky ..)
sys.path.insert(0, str(backend_dir))