# Test script for KeyGenie setup
import importlib
import sys
from database import init_db

modules = ["bot", "config", "database", "admin"]

print("Testing module imports...")
for m in modules:
    try:
        importlib.import_module(m)
        print(f"{m} import: OK")
    except Exception as e:
        print(f"{m} import: FAIL — {e}")
        sys.exit(1)

print("Initializing database...")
try:
    init_db()
    print("Database initialization: OK")
except Exception as e:
    print(f"Database initialization: FAIL — {e}")
    sys.exit(1)

print("All tests passed.")
