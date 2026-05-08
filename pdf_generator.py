"""
PDF generator for Sterling Sovereign profiles.
Uses WeasyPrint (HTML → PDF) for pixel-perfect luxury output.
"""

from jinja2 import Environment, FileSystemLoader
import weasyprint
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def generate_pdf(data: dict, output_path: str) -> None:
    """Render the Jinja2 HTML template with profile data and export to PDF."""
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("profile.html")
    html_content = template.render(**data)

    weasyprint.HTML(string=html_content, base_url=TEMPLATE_DIR).write_pdf(output_path)
