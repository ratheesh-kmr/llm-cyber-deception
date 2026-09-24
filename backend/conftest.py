import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))

# Clean sys.path of external 'Lenny Growth Assistant' paths
sys.path = [p for p in sys.path if "Lenny Growth Assistant" not in p]
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def pytest_configure(config):
    sys.path = [p for p in sys.path if "Lenny Growth Assistant" not in p]
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    for mod in list(sys.modules.keys()):
        if mod == 'app' or mod.startswith('app.'):
            del sys.modules[mod]
