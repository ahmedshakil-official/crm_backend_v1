from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Dict, Optional

from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone

from weasyprint import HTML, CSS

@dataclass
class ReportColumn:
    key: str
    label: str

class ReportRendererMixin:
    """
    Renders a modern PDF using HTML/CSS and WeasyPrint.
    """

    base_template = "report.html"  # add this file below

    def render_pdf(self, request, context: dict, filename: str) -> HttpResponse:
        """
        Renders the given context into a PDF using the configured template.
        """
        template = get_template(self.base_template)
        html_str = template.render(context | {"current_time": timezone.localtime()})
        html = HTML(string=html_str, base_url=request.build_absolute_uri("/"))

        # Minimal, classy page setup; additional styles in the template itself
        css = CSS(string="""
            @page { size: A4; margin: 18mm 14mm 18mm 14mm; }
            @page {
              @bottom-right { content: "Page " counter(page) " of " counter(pages); font-size: 10px; color: #6b7280; }
            }
        """)

        pdf_bytes = html.write_pdf(stylesheets=[css])

        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'
        return resp
