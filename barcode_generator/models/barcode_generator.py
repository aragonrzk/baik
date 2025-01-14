from odoo import models, fields, api
from datetime import datetime, timedelta
import qrcode
import base64
import io
import barcode
from barcode.writer import ImageWriter

class BarcodeGenerator(models.Model):
    _name = 'barcode.generator'
    _description = 'Barcode and QR Code Generator'

    name = fields.Char(string='Nama', required=True)
    date_from = fields.Date(string='Dari Tgl', required=True)
    date_to = fields.Date(string='Ke Tgl', required=True)
    barcode_type = fields.Selection([
        ('barcode', 'Barcode'),
        ('qrcode', 'QR Code'),
        ('both', 'Both')
    ], string='Tipe', default='both', required=True)
    price = fields.Float(string='Harga', required=True) 
    generated_code_ids = fields.One2many('barcode.generator.line', 'generator_id', string='Generated Codes')
    
    @api.model
    def create(self, vals):
        record = super(BarcodeGenerator, self).create(vals)
        record.generate_codes()
        return record
    
    def unlink(self):
        # Sebelum menghapus, hapus data terkait di barcode.generator.line
        for record in self:
            record.generated_code_ids.unlink()  # Menghapus data terkait secara eksplisit
        return super(BarcodeGenerator, self).unlink()
    
    def generate_codes(self):
        for record in self:
            # Clear existing codes
            record.generated_code_ids.unlink()
            
            current_date = record.date_from
            count = 1
            while current_date <= record.date_to:
                date_str = current_date.strftime('%Y%m%d')
                generate_code = f"{record.name}-{date_str}-{count}"
                vals = {
                    'generator_id': record.id,
                    'date': current_date,
                    'price': record.price, #tambahkan field price ke vals
                    'name': record.name,
                    'generate_code': generate_code,
                }
                
                if record.barcode_type in ['barcode', 'both']:
                    # Generate Barcode
                    CODE128 = barcode.get_barcode_class('code128')
                    rv = io.BytesIO()
                    CODE128(generate_code, writer=ImageWriter()).write(rv)
                    vals['barcode_data'] = base64.b64encode(rv.getvalue())
                
                if record.barcode_type in ['qrcode', 'both']:
                    # Generate QR Code
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(generate_code)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    temp = io.BytesIO()
                    img.save(temp, format="PNG")
                    vals['qrcode_data'] = base64.b64encode(temp.getvalue())
                
                self.env['barcode.generator.line'].create(vals)
                current_date += timedelta(days=1)
                count += 1

    def print_report(self):
        # arahkan ke metode preview sebelum cetak
        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': '/web/content/' + str(self.id) + '/barcode_report',
        #     'target': 'new',
        # }
        
        return self.env.ref('barcode_generator.action_report_barcodegenerator').report_action(self)
        

class BarcodeGeneratorLine(models.Model):
    _name = 'barcode.generator.line'
    _description = 'Generated Barcode and QR Code Lines'
    
    generator_id = fields.Many2one('barcode.generator', string='Generator', required=True)
    date = fields.Date(string='Date', required=True)
    barcode_data = fields.Binary(string='Barcode', attachment=True)
    qrcode_data = fields.Binary(string='QR Code', attachment=True)
    price = fields.Float(String='Harga', required=True)
    name = fields.Char(string='Nama', required=True)
    generate_code = fields.Char(string='Generate Code', required=True)