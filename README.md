# mcg-agent-hub

Quick start

1. Activate the virtual environment (created in this workspace):

```bash
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app (assumes an ASGI app instance named `app` in `main.py`):

```bash
uvicorn main:app --reload --port 8000
```

Notes

- If you need Google GenAI credentials, set the appropriate environment variables (for example `GOOGLE_API_KEY` or `GOOGLE_APPLICATION_CREDENTIALS`) before running the app.
- If `main.py` exposes a different ASGI variable, update the `uvicorn` command accordingly.
