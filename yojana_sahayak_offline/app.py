from pathlib import Path
import json
from typing import Optional
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse

BASE = Path(__file__).resolve().parent
DATA_FILE = BASE / "data" / "scholarships.json"
app = FastAPI(title="Yojana Sahayak - Offline Prototype")

with DATA_FILE.open("r", encoding="utf-8") as f:
    SCHOLARSHIPS = json.load(f)


def norm(value: str) -> str:
    return (value or "").strip().lower()


def matches(s, education="", category="", income=None):
    ok = True
    if education:
        edu = norm(education)
        allowed = [norm(x) for x in s.get("education", [])]
        ok = ok and ("all" in allowed or edu in allowed)
    if category:
        cat = norm(category)
        allowed = [norm(x) for x in s.get("categories", [])]
        ok = ok and ("all" in allowed or cat in allowed)
    if income is not None:
        max_income = s.get("max_income")
        if max_income is not None:
            ok = ok and income <= max_income
    return ok


def format_results(results):
    if not results:
        return ("I couldn't find a matching scholarship in the prototype database. "
                "Try another education level, category, or income range.\n\n"
                "Note: This offline prototype uses a small demonstration dataset.")
    lines = [f"I found {len(results)} possible match{'es' if len(results) != 1 else ''}:\n"]
    for i, s in enumerate(results, 1):
        lines.append(f"🎓 {i}. {s['name']}")
        lines.append(f"   {s['short_description']}")
        lines.append(f"   Eligibility: {s['eligibility']}")
        lines.append(f"   Documents: {', '.join(s['documents'])}")
        lines.append(f"   Apply: {s['official_link']}\n")
    lines.append("⚠️ This is preliminary guidance only. Check the official scheme website before applying.")
    return "\n".join(lines)


@app.get("/")
def home():
    return FileResponse(BASE / "static" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "mode": "offline-prototype"}


@app.get("/api/scholarships")
def scholarships():
    return SCHOLARSHIPS


@app.get("/api/match")
def match(
    education: str = Query(""),
    category: str = Query(""),
    income: Optional[float] = Query(None),
):
    results = [s for s in SCHOLARSHIPS if matches(s, education, category, income)]
    return {"message": format_results(results), "results": results}


@app.get("/api/chat")
def chat(message: str = Query("")):
    text = norm(message)
    if any(w in text for w in ["hello", "hi", "hey", "namaste"]):
        return {"reply": "Hello! 👋 I am Yojana Sahayak. Tell me your education level, category and family income, or use the profile form to find scholarships."}
    if "document" in text or "docs" in text:
        return {"reply": "Common documents may include marksheets, income certificate, caste/category certificate where applicable, domicile proof and bank details required by the official portal. Always verify the exact list on the official scheme page."}
    if "apply" in text or "application" in text:
        return {"reply": "For this prototype, use the official application link shown with each matching scholarship. The chatbot does not submit an application."}
    if "scholarship" in text or "student" in text:
        return {"reply": "I can help with preliminary scholarship matching. Enter your profile on the right and click Find Scholarships."}
    return {"reply": "I can help you find scholarships. Try: 'I am a 12th pass student' or use the profile form to provide education, category and family income."}
