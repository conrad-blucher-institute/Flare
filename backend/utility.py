from datetime import datetime
import sys
import inspect
import traceback

_current_chart_name = "unknown_chart"

def set_current_chart_name(name: str):
    global _current_chart_name
    if not name or not name.strip():
        name = "unknown_chart"
    _current_chart_name = name.strip()

def get_current_chart_name() -> str:
    return _current_chart_name

def log_info(message: str) -> None:
    """Logs an info-level message to stdout with timestamp."""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"[{timestamp}] {message}", file=sys.stdout)

def log_error(message: str,chart_name: str,error_type: str = "ERROR",include_traceback: bool = False ) -> None:
    """Logs an error-level message to stderr with timestamp."""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    # Get the caller's location
    frame = inspect.currentframe().f_back
    location = f"{frame.f_globals.get('__name__', '__main__')}::{frame.f_code.co_name}()"

    print(file=sys.stderr)  # Blank line for spacing
    print("=" * 80, file=sys.stderr)
    print(f"[{timestamp}] {error_type}", file=sys.stderr)
    print(f"Location    : {location}", file=sys.stderr)
    print(f"ChartName   : {chart_name}", file=sys.stderr)
    print(f"Message     : {message}", file=sys.stderr)

    if include_traceback:
        tb = traceback.format_exc()
        if tb.strip() != "NoneType: None":
            print("Traceback   :", file=sys.stderr)
            print(tb, file=sys.stderr)

    print("=" * 80, file=sys.stderr)
    print(file=sys.stderr)
    
    