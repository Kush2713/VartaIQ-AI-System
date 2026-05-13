import sys

# Guard: ML packages (torch, numpy, spacy) require Python 3.10-3.12
if sys.version_info >= (3, 13):
    print(
        f"\n[ERROR] Python {sys.version_info.major}.{sys.version_info.minor} is not supported.\n"
        "Please use Python 3.10, 3.11, or 3.12.\n"
        "Run: py -3.10 -m venv venv  (then reinstall requirements)\n"
    )
    sys.exit(1)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
