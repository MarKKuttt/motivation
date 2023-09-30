import io
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Dict, Any

from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


LOCAL_FILE_PATH = 'data/FreeSans.ttf'
PARENT_PATH = Path(__file__).resolve().parent.parent.parent
pdfmetrics.registerFont(TTFont('FreeSans', PARENT_PATH / LOCAL_FILE_PATH))


@dataclass
class PDFTemplate:
    """Template for PDF file (ShoppingCart)."""

    HEADER = "Список покупок"
    BUFFER = io.BytesIO()
    CANVAS = canvas.Canvas(BUFFER, pagesize=letter, bottomup=0)
    TEXT_OBJ = CANVAS.beginText()
    TEXT_OBJ.setTextOrigin(inch, inch)
    TEXT_OBJ.setFont("FreeSans", 14)

    def fill(self, queryset: Iterable[Dict[str, Any]]):
        self.TEXT_OBJ.textLine(self.HEADER)
        for query_element in queryset:
            line_representation: str = ' '.join(map(str, [*query_element.values()]))
            self.TEXT_OBJ.textLine(line_representation)
        self.CANVAS.drawText(self.TEXT_OBJ)
        self.CANVAS.showPage()
        self.CANVAS.save()
        self.BUFFER.seek(0)
        return FileResponse(
            self.BUFFER, as_attachment=True, filename=f"{self.HEADER}.pdf"
        )
