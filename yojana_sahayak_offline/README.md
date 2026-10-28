# Yojana Sahayak — Offline WhatsApp-Style Prototype

This version does **not** require Meta WhatsApp Cloud API, a WhatsApp phone number, access tokens, or webhook setup.

It provides a WhatsApp-style browser interface connected to a small local scholarship demonstration dataset through FastAPI.

## Run on your laptop

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
uvicorn app:app --reload
```

5. Open:

`http://127.0.0.1:8000`

## Render deployment (optional)

Create a Render Web Service from this folder/repository.

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- **No environment variables are required.**

## Important project note

The scholarship records in `data/scholarships.json` are explicitly **DEMO records** for a prototype. They should not be presented as verified current scholarship rules. For a final project version, replace them with reviewed official scheme records and keep the official source links/review dates.

The prototype provides preliminary guidance only. It does not make an official eligibility decision and does not submit applications.

## Project alignment

The interface demonstrates the report's proposed flow: a student provides profile information, the assistant identifies possible scheme records, explains indicative eligibility/documents, and points to an official application/source route.

Meta WhatsApp Cloud API can be integrated later as a separate channel if required.
