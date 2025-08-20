import sys
from pathlib import Path

# Add backend folder to path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))