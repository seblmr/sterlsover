from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Monter le dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rediriger la racine vers la landing page
@app.get("/")
def root():
    return FileResponse("static/index.html")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
import anthropic
import json
import uuid
import os
from datetime import datetime
from pdf_generator import generate_pdf
from prompt import build_prompt

app = FastAPI(title="Sterling Sovereign API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restreindre en prod
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# ── Schémas ────────────────────────────────────────────────────────────
class ProfileRequest(BaseModel):
    email: EmailStr
    full_name: str
    linkedin_url: str | None = None
    company: str | None = None
    sector: str | None = None
    annual_revenue: str | None = None   # ex: "100k-500k", "1M-5M"
    years_experience: int | None = None
    founded_companies: int | None = 0
    ambition_statement: str | None = None   # "Décrire ton ambition en 1 phrase"
    tier: str = "duke"   # baron | duke | chancellor


class ProfileResponse(BaseModel):
    profile_id: str
    pdf_url: str
    summary: dict


# ── Endpoint principal ─────────────────────────────────────────────────
@app.post("/generate-profile", response_model=ProfileResponse)
async def generate_profile(req: ProfileRequest):
    profile_id = str(uuid.uuid4())[:8].upper()

    # 1. Construire le prompt et appeler Claude
    prompt = build_prompt(req)
    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = message.content[0].text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Claude API error: {str(e)}")

    # 2. Parser le JSON retourné par Claude
    try:
        # Nettoyer les éventuels backticks markdown
        clean = raw.strip().lstrip("```json").rstrip("```").strip()
        profile_data = json.loads(clean)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse Claude response")

    # Injecter les métadonnées
    profile_data["member_id"]   = f"#{profile_id}"
    profile_data["tier"]        = req.tier.capitalize()
    profile_data["full_name"]   = req.full_name
    profile_data["generated_at"] = datetime.utcnow().strftime("%d %B %Y")

    # 3. Générer le PDF
    pdf_path = f"/tmp/sovereign_{profile_id}.pdf"
    generate_pdf(profile_data, pdf_path)

    # Exposer le PDF via l'endpoint /download
    return ProfileResponse(
        profile_id=profile_id,
        pdf_url=f"/download/{profile_id}",
        summary={
            "prestige_score":  profile_data.get("prestige_score"),
            "archetype":       profile_data.get("archetype"),
            "rank":            profile_data.get("rank"),
            "motto_latin":     profile_data.get("motto_latin"),
        }
    )


@app.get("/download/{profile_id}")
def download_pdf(profile_id: str):
    path = f"/tmp/sovereign_{profile_id}.pdf"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Profile not found")
    return FileResponse(path, media_type="application/pdf",
                        filename=f"sterling_sovereign_{profile_id}.pdf")


@app.get("/health")
def health():
    return {"status": "sovereign", "timestamp": datetime.utcnow().isoformat()}

