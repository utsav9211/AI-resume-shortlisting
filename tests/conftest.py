# conftest.py
# Add project root to sys.path so tests can import `app` and `src` modules
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
