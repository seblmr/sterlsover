import os
import base64
from pathlib import Path
from mailjet_rest import Client

MJ_API_KEY    = os.environ.get("MAILJET_API_KEY")
MJ_API_SECRET = os.environ.get("MAILJET_API_SECRET")

FROM_EMAIL = os.environ.get("FROM_EMAIL", "profiles@sterling-sovereign.co.uk")
FROM_NAME  = "Sterling Sovereign"

TIER_LABELS = {
    "baron":      "Baron",
    "duke":       "Duke",
    "chancellor": "Chancellor",
}


def send_profile_email(
    to_email: str,
    full_name: str,
    profile_id: str,
    tier: str,
    prestige_score: int,
    archetype: str,
    rank: str,
    motto_latin: str,
    motto_english: str,
    pdf_path: str,
    pdf_url: str,
    base_url: str,
) -> dict:

    first_name    = full_name.split()[0] if full_name else "Founder"
    tier_label    = TIER_LABELS.get(tier, tier.capitalize())
    download_link = f"{base_url}{pdf_url}"

    pdf_bytes = Path(pdf_path).read_bytes()
    pdf_b64   = base64.b64encode(pdf_bytes).decode()

    html_body = (
        '<!DOCTYPE html><html lang="en"><head>'
        '<meta charset="UTF-8"/>'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0"/>'
        '</head>'
        '<body style="margin:0;padding:0;background:#06050a;font-family:Georgia,serif;color:#f0e6cf;">'
        '<table width="100%" cellpadding="0" cellspacing="0" style="background:#06050a;padding:48px 20px;">'
        '<tr><td align="center">'
        '<table width="580" cellpadding="0" cellspacing="0" style="max-width:580px;width:100%;">'

        # Header
        '<tr><td style="border-bottom:1px solid rgba(201,168,76,.2);padding-bottom:28px;text-align:center;">'
        '<p style="font-size:10px;letter-spacing:6px;color:#6b5119;text-transform:uppercase;margin:0 0 16px;">EST. MMXXV &mdash; LONDON, EC2</p>'
        '<p style="font-size:22px;letter-spacing:4px;color:#c9a84c;margin:0;font-weight:normal;">STERLING SOVEREIGN</p>'
        '</td></tr>'

        # Hero
        '<tr><td style="padding:44px 0 32px;text-align:center;">'
        '<p style="font-size:10px;letter-spacing:5px;color:#a07a2a;margin:0 0 24px;text-transform:uppercase;">Sovereign Profile &mdash; ' + tier_label + '</p>'
        '<h1 style="font-size:36px;font-weight:300;color:#f0e6cf;margin:0 0 8px;line-height:1.1;">' + first_name + ',</h1>'
        '<h2 style="font-size:26px;font-weight:300;font-style:italic;color:#c9a84c;margin:0 0 32px;">your profile has been forged.</h2>'
        '<p style="font-style:italic;font-size:15px;color:rgba(240,230,207,.6);margin:0 auto;line-height:1.7;max-width:380px;">'
        'The AI has consulted the archives. Your sovereign wealth identity is enclosed.</p>'
        '</td></tr>'

        # Score band
        '<tr><td style="padding:0 0 32px;">'
        '<table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid rgba(201,168,76,.15);">'
        '<tr>'
        '<td width="33%" style="padding:22px 16px;text-align:center;border-right:1px solid rgba(201,168,76,.12);">'
        '<p style="font-size:34px;font-weight:300;color:#c9a84c;margin:0;line-height:1;">' + str(prestige_score) + '</p>'
        '<p style="font-size:8px;letter-spacing:3px;color:#6e6358;margin:6px 0 0;text-transform:uppercase;">Prestige Score</p>'
        '</td>'
        '<td width="33%" style="padding:22px 16px;text-align:center;border-right:1px solid rgba(201,168,76,.12);">'
        '<p style="font-size:16px;font-weight:300;color:#c9a84c;margin:0;">' + rank + '</p>'
        '<p style="font-size:8px;letter-spacing:3px;color:#6e6358;margin:6px 0 0;text-transform:uppercase;">Order Rank</p>'
        '</td>'
        '<td width="33%" style="padding:22px 16px;text-align:center;">'
        '<p style="font-size:14px;font-weight:300;color:#c9a84c;margin:0;">' + tier_label + '</p>'
        '<p style="font-size:8px;letter-spacing:3px;color:#6e6358;margin:6px 0 0;text-transform:uppercase;">Profile Tier</p>'
        '</td>'
        '</tr></table></td></tr>'

        # Archetype + motto
        '<tr><td style="padding:0 0 32px;">'
        '<table width="100%" cellpadding="0" cellspacing="0" style="background:#0f0d14;border:1px solid rgba(201,168,76,.1);">'
        '<tr><td style="padding:28px 32px;">'
        '<p style="font-size:8px;letter-spacing:5px;color:#c9a84c;text-transform:uppercase;margin:0 0 10px;">Your Archetype</p>'
        '<p style="font-size:20px;color:#f0e6cf;margin:0 0 16px;">' + archetype + '</p>'
        '<table cellpadding="0" cellspacing="0"><tr>'
        '<td style="border-left:2px solid #c9a84c;padding:8px 16px;">'
        '<p style="font-style:italic;font-size:15px;color:#e8cc82;margin:0 0 4px;">&ldquo;' + motto_latin + '&rdquo;</p>'
        '<p style="font-size:10px;letter-spacing:2px;color:#6e6358;margin:0;text-transform:uppercase;">' + motto_english + '</p>'
        '</td></tr></table>'
        '</td></tr></table></td></tr>'

        # CTA button
        '<tr><td style="padding:0 0 40px;text-align:center;">'
        '<p style="font-style:italic;font-size:15px;color:rgba(240,230,207,.55);margin:0 0 28px;line-height:1.7;">'
        'Your full profile &mdash; Coat of Arms, Dynasty Blueprint<br>'
        'and Board of Invisible Advisors &mdash; is attached to this email.</p>'
        '<a href="' + download_link + '" '
        'style="display:inline-block;font-size:11px;letter-spacing:3px;color:#06050a;'
        'background:#c9a84c;text-decoration:none;padding:16px 44px;text-transform:uppercase;">'
        'Download PDF Profile</a>'
        '</td></tr>'

        # Footer
        '<tr><td style="border-top:1px solid rgba(201,168,76,.12);padding-top:28px;text-align:center;">'
        '<p style="font-size:8px;letter-spacing:4px;color:#6b5119;text-transform:uppercase;margin:0 0 8px;">'
        'Member #' + profile_id + ' &mdash; Order of Sovereigns</p>'
        '<p style="font-style:italic;font-size:11px;color:rgba(110,99,88,.6);margin:0;line-height:1.6;">'
        'For entertainment and inspirational purposes. Not financial advice.<br>'
        '&copy; Sterling Sovereign MMXXV &mdash; London</p>'
        '</td></tr>'

        '</table></td></tr></table></body></html>'
    )

    text_body = "\n".join([
        "STERLING SOVEREIGN",
        f"Member #{profile_id} -- {tier_label}",
        "",
        f"{first_name},",
        "Your sovereign profile has been forged.",
        "",
        f"PRESTIGE SCORE : {prestige_score}",
        f"RANK           : {rank}",
        f"ARCHETYPE      : {archetype}",
        f'MOTTO          : "{motto_latin}" -- {motto_english}',
        "",
        f"Download : {download_link}",
        "",
        "--",
        "Sterling Sovereign -- For entertainment purposes. Not financial advice.",
    ])

    mailjet = Client(auth=(MJ_API_KEY, MJ_API_SECRET), version="v3.1")

    data = {
        "Messages": [{
            "From": {
                "Email": FROM_EMAIL,
                "Name":  FROM_NAME,
            },
            "To": [{
                "Email": to_email,
                "Name":  full_name,
            }],
            "Subject":  f"Your Sovereign Profile is ready, {first_name} -- Member #{profile_id}",
            "HTMLPart": html_body,
            "TextPart": text_body,
            "Attachments": [{
                "ContentType":   "application/pdf",
                "Filename":      f"sterling_sovereign_{profile_id}.pdf",
                "Base64Content": pdf_b64,
            }],
        }]
    }

    result = mailjet.send.create(data=data)

    if result.status_code != 200:
        raise RuntimeError(f"Mailjet error {result.status_code}: {result.json()}")

    return result.json()
