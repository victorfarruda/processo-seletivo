from reportlab.lib.units import mm
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import HorizontalBarChart


class criar_codigo_barras(Drawing):
    def __init__(self, text_value, *args, **kw):
        if len(text_value) > 10:
            raise ValueError
        if len(text_value) < 10:
            while len(text_value) < 10:
                text_value = '0' + text_value
        barcode = createBarcodeDrawing('Code128', value=text_value, barHeight=20 * mm, humanReadable=True)
        Drawing.__init__(self, barcode.width, barcode.height, *args, **kw)
        self.add(barcode, name='barcode')
