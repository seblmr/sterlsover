# Sterling Sovereign — Backend

## Structure

```
sovereign/
├── main.py              # FastAPI app + endpoints
├── prompt.py            # Prompt engineering (Claude)
├── pdf_generator.py     # WeasyPrint HTML→PDF
├── requirements.txt
└── templates/
    └── profile.html     # Template PDF Jinja2 (noir & or)
```

## Installation

```bash
pip install -r requirements.txt
```

Sur Debian/Ubuntu, WeasyPrint nécessite :
```bash
apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

## Variables d'environnement

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## Lancement local

```bash
uvicorn main:app --reload --port 8000
```

## Déploiement Coolify

1. Push le repo sur GitHub
2. Dans Coolify : New Service → Dockerfile ou Nixpacks
3. Ajouter la variable `ANTHROPIC_API_KEY` dans les env vars
4. Exposer le port 8000

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/generate-profile` | Génère le profil + PDF |
| GET | `/download/{id}` | Télécharge le PDF |
| GET | `/health` | Status check |

## Exemple de requête

```bash
curl -X POST http://localhost:8000/generate-profile \
  -H "Content-Type: application/json" \
  -d '{
    "email": "founder@example.com",
    "full_name": "Alexandre Whitmore",
    "company": "Whitmore Ventures",
    "sector": "FinTech",
    "annual_revenue": "1M-5M",
    "years_experience": 8,
    "founded_companies": 2,
    "ambition_statement": "Build the next European financial empire.",
    "tier": "duke"
  }'
```

## Tiers disponibles

| Tier | Prix | Pages PDF | Sections |
|------|------|-----------|----------|
| baron | £9 | 2 | Score, Archetype, Motto, Strengths |
| duke | £29 | 3 | + Blueprint, Advisors, Crest, Bloodline |
| chancellor | £99 | 4 | + Reputation, Brand Brief, Network |
