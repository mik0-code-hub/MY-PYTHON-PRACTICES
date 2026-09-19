import os
import sys
import uvicorn

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    print("=" * 60)
    print("  DANGOTE GROUP ENTERPRISE CORPORATE PORTAL")
    print("  Providing Your Basic Needs Across Africa")
    print("=" * 60)
    print("  Server launching on: http://127.0.0.1:8000")
    print("=" * 60)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
