"""
Prompt builder for Sterling Sovereign profile generation.
Returns a prompt that instructs Claude to output strict JSON.
"""


TIER_SECTIONS = {
    "baron": ["prestige_score", "archetype", "rank", "motto_latin", "motto_english",
              "archetype_description", "core_strengths"],
    "duke":  ["prestige_score", "archetype", "rank", "motto_latin", "motto_english",
              "archetype_description", "core_strengths", "wealth_projection_10y",
              "dynasty_blueprint", "invisible_advisors", "coat_of_arms_description",
              "founder_bloodline_score"],
    "chancellor": ["prestige_score", "archetype", "rank", "motto_latin", "motto_english",
                   "archetype_description", "core_strengths", "wealth_projection_10y",
                   "dynasty_blueprint", "invisible_advisors", "coat_of_arms_description",
                   "founder_bloodline_score", "reputation_strategy", "personal_brand_brief",
                   "network_gravity_analysis"],
}

ARCHETYPE_LIST = [
    "The Architect Sovereign",
    "The Disruptor Baron",
    "The Stoic Patriarch",
    "The Visionary Alchemist",
    "The Silent Empire Builder",
    "The Renaissance Operator",
    "The Relentless Ascendant",
    "The Gilded Strategist",
    "The Iron Merchant",
    "The Luminous Founder",
]

RANK_TIERS = {
    "baron":      ["Esquire", "Knight", "Baron"],
    "duke":       ["Viscount", "Earl", "Marquess", "Duke"],
    "chancellor": ["Prince", "Chancellor", "Sovereign"],
}


def build_prompt(req) -> str:
    tier = req.tier.lower() if req.tier.lower() in TIER_SECTIONS else "duke"
    sections = TIER_SECTIONS[tier]
    ranks    = RANK_TIERS[tier]

    user_context = f"""
Founder Profile:
- Name: {req.full_name}
- Company / Sector: {req.company or 'Undisclosed'} / {req.sector or 'Undisclosed'}
- Annual Revenue: {req.annual_revenue or 'Not disclosed'}
- Years of Experience: {req.years_experience or 'Not specified'}
- Companies Founded: {req.founded_companies or 0}
- Ambition Statement: "{req.ambition_statement or 'To build a lasting empire.'}"
- LinkedIn: {req.linkedin_url or 'Not provided'}
    """.strip()

    sections_desc = _describe_sections(sections, ranks)

    return f"""You are the sovereign intelligence engine of Sterling Sovereign, an elite AI wealth identity service for founders. Your role is to generate a prestige founder profile — rich in narrative gravitas, psychological depth, and aspirational language.

This is an entertainment and identity product. Be bold, flattering, precise, and aristocratic in tone. You are not providing financial advice — you are crafting a mirror that reflects a founder's highest potential self.

{user_context}

Generate a JSON profile with EXACTLY these fields:
{sections_desc}

CRITICAL RULES:
1. Return ONLY valid JSON. No preamble, no markdown, no explanation.
2. Every field must be present.
3. Tone: aristocratic, precise, aspirational. Think The Economist meets a medieval herald.
4. prestige_score: integer between 62 and 97 — calibrated to feel earned, never arbitrary.
5. archetype: choose the most fitting from {ARCHETYPE_LIST}
6. rank: choose from {ranks} — the highest rank should be rare.
7. motto_latin: an original, meaningful Latin phrase (not a cliché).
8. wealth_projection_10y: a specific £ figure with narrative context (e.g. "£4.2M — built through compounding equity and network leverage").
9. invisible_advisors: array of 3 objects with "name", "era", and "counsel" fields.
10. coat_of_arms_description: vivid heraldic description (colours, animals, symbols, motto placement).
11. dynasty_blueprint: 3-5 sentence strategic narrative for the next decade.
12. founder_bloodline_score: integer 55-94 representing alignment with self-made dynasty archetypes.
13. reputation_strategy (chancellor only): 3-4 sentence public positioning strategy.
14. personal_brand_brief (chancellor only): object with "headline", "positioning", "tone_of_voice" fields.
15. network_gravity_analysis (chancellor only): description of the founder's natural network pull and ideal inner circle profile.

JSON structure example for orientation (adapt fields to the tier):
{{
  "prestige_score": 84,
  "archetype": "The Architect Sovereign",
  "rank": "Duke",
  "motto_latin": "Per ardua, per aurum",
  "motto_english": "Through hardship, through gold",
  "archetype_description": "...",
  "core_strengths": ["Capital Vision", "Systemic Thinking", "Relentless Execution"],
  "founder_bloodline_score": 79,
  "wealth_projection_10y": "£6.1M — ...",
  "dynasty_blueprint": "...",
  "coat_of_arms_description": "...",
  "invisible_advisors": [
    {{"name": "Andrew Carnegie", "era": "1880s–1910s", "counsel": "..."}},
    {{"name": "Coco Chanel", "era": "1920s", "counsel": "..."}},
    {{"name": "Elon Musk", "era": "Present", "counsel": "..."}}
  ]
}}

Now generate the full profile for the founder above. Return JSON only.
"""


def _describe_sections(sections: list, ranks: list) -> str:
    desc = {
        "prestige_score":           "integer (62–97): overall founder prestige rating",
        "archetype":                "string: founder archetype name",
        "rank":                     f"string: aristocratic rank from {ranks}",
        "motto_latin":              "string: original Latin motto",
        "motto_english":            "string: English translation of the motto",
        "archetype_description":    "string (2–3 sentences): rich description of this archetype",
        "core_strengths":           "array of 3–5 strings: key founder strengths",
        "founder_bloodline_score":  "integer (55–94): dynasty alignment score",
        "wealth_projection_10y":    "string: projected wealth figure + 1-sentence narrative",
        "dynasty_blueprint":        "string (3–5 sentences): 10-year strategic narrative",
        "coat_of_arms_description": "string: heraldic description of the AI-generated crest",
        "invisible_advisors":       'array of 3 advisor objects with "name", "era", "counsel"',
        "reputation_strategy":      "string (3–4 sentences): public positioning strategy",
        "personal_brand_brief":     'object with "headline", "positioning", "tone_of_voice"',
        "network_gravity_analysis": "string (2–3 sentences): network pull analysis",
    }
    lines = [f'- "{s}": {desc[s]}' for s in sections if s in desc]
    return "\n".join(lines)
