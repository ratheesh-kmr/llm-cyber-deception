import sys
import os

# Ensure backend/ and project root are in sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)

sys.path = [p for p in sys.path if "Lenny Growth Assistant" not in p]
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Clear any cached external app modules
for mod in list(sys.modules.keys()):
    if mod == 'app' or mod.startswith('app.'):
        del sys.modules[mod]

import uvicorn

if __name__ == "__main__":
    from app.main import app
    print("Starting Cyber Deception Platform Backend API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
