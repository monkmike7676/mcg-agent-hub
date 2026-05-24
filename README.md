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

Email test

- Copy `.env.example` to `.env` and fill in your email settings.
- Do not check `.env` into version control.
- By default, the test script now uses the Gmail API when `USE_GMAIL_API=true`.
- Place your OAuth client credentials in `credentials.json` and authorize the script the first time it runs.
- Send a test buyer inquiry email with:

```bash
python send_test_email.py
```

Gmail API setup

1. In Google Cloud Console, create OAuth 2.0 Client Credentials for a desktop application.
2. Download and save the JSON file to `credentials.json` in this project root.
3. Set `USE_GMAIL_API=true` in `.env`.
4. Run `python send_test_email.py` and complete the browser authorization flow.

Notes

- If you need Google GenAI credentials, set the appropriate environment variables (for example `GOOGLE_API_KEY` or `GOOGLE_APPLICATION_CREDENTIALS`) before running the app.
- For Gemini, create a local `.env` file with `GEMINI_API_KEY` and load it before running your app. This `.env` file is ignored by Git.
- `main.py` automatically loads `.env` using `python-dotenv`, so `GEMINI_API_KEY` will be available at runtime.
- If `main.py` exposes a different ASGI variable, update the `uvicorn` command accordingly.
