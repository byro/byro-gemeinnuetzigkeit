from reportlab.lib import utils
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, Image, PageTemplate

FONTSIZE = 11
PAGESIZE = portrait(A4)
CURRENCY = '{:.2f} €'


def get_paragraph_style():
    style = getSampleStyleSheet()
    # TODO: font
    # style.fontName = 'OpenSans'
    style['Normal'].fontSize = FONTSIZE
    style['Normal'].leading = int(1.5 * FONTSIZE)
    return style


def scale_image(fileish, width: int) -> Image:
    """ scales image with given width. fileish may be file or path """
    img = utils.ImageReader(fileish)
    orig_width, height = img.getSize()
    aspect = height / orig_width
    return Image(fileish, width=width, height=width * aspect)


def get_default_document(_buffer, footer: str=None) -> BaseDocTemplate:
    def on_page(canvas, doc, footer=footer):
        canvas.saveState()
        if footer:
            canvas.setFontSize(8)
            for i, line in enumerate(footer.split('\n')[::-1]):
                canvas.drawCentredString(PAGESIZE[0] / 2, 25 + (3.5 * i) * mm, line.strip())
            canvas.restoreState()

    doc = BaseDocTemplate(
        _buffer,
        pagesize=PAGESIZE,
        leftMargin=25 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='normal')
    doc_template = PageTemplate(id='all', pagesize=PAGESIZE, frames=[frame], onPage=on_page)
    doc.addPageTemplates([doc_template])
    return doc
