# controllers/barcode_generator.py
from odoo import http
from odoo.http import request

class BarcodeGeneratorController(http.Controller):
    @http.route('/barcode_report', auth='public')
    def barcode_report_preview(self, barcode_id, **kwargs):
        barcode = request.env['barcode.generator'].browse(int(barcode_id))
        return request.render('barcode_generator.report_barcodegenerator', {'doc': barcode})
