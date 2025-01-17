from odoo import models, fields, api
from odoo.exceptions import UserError  # Import untuk popup Warning
# from itertools import groupby
# from operator import itemgetter
import logging
_logger = logging.getLogger(__name__)
    

class Scanner(models.Model):
    _name = 'scanner.scanner'
    _description = 'Scanner Codabar'

    barcode = fields.Char(string='Codabar', required=False)   
    price = fields.Float(string='Price', readonly=True, required=False)
    name = fields.Char(string='Name', readonly=True , required=False)
    
    # Menambahkan fields baru
    scanner_line_ids = fields.One2many('scanner.line', 'scanner_id', string='Scan Lines')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    
    
    
    @api.depends('scanner_line_ids.price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.scanner_line_ids.mapped('price'))    
            
   
   
    @api.onchange('barcode')
    def _onchange_barcode(self):
         if self.barcode:
            # Cari data berdasarkan generate_code
            generate_code_record = self.env['barcode.generator.line'].search([
                ('generate_code', '=', self.barcode)
            ], limit=1)

            if generate_code_record:
                # Check apakah barcode dan name sudah ada di scanner_line_ids
                existing_line = self.scanner_line_ids.filtered(
                    lambda line: line.barcode.startswith(generate_code_record.generate_code) and line.name == generate_code_record.name
                )

                if existing_line:
                    # Update baris yang sudah ada
                    existing_line.price += generate_code_record.price
                    # Update barcode dengan menambahkan jumlah scan (x)
                    current_count = int(existing_line.barcode.split('(')[-1][:-1]) if '(' in existing_line.barcode else 1
                    existing_line.barcode = f"{generate_code_record.generate_code}({current_count + 1})"
                else:
                    # Tambahkan baris baru
                    vals = {
                        'barcode': generate_code_record.generate_code + '(1)',
                        'price': generate_code_record.price,
                        'name': generate_code_record.name,
                    }
                    self.scanner_line_ids = [(0, 0, vals)]
                
                # Kosongkan input setelah proses selesai
                self.price = generate_code_record.price
                self.name = generate_code_record.name
            else:
                # Jika tidak ditemukan, tampilkan popup dengan pesan
                raise UserError(f'Data tidak ditemukan untuk barcode: {self.barcode}')
                self.price = 0
                self.name = ''
            
            # Kosongkan barcode input
            self.barcode = ''
        # if self.barcode:
        #     # Cari data berdasarkan generate_code
        #     generate_code_record = self.env['barcode.generator.line'].search([
        #         ('generate_code', '=', self.barcode)  # Ganti 'generate_code' dengan nama field yang benar
        #     ], limit=1)

        #     if generate_code_record:
        #         self.price = generate_code_record.price
        #         self.name = generate_code_record.name

              
        #         vals = {
        #             'barcode': self.barcode,
        #             'price': self.price,
        #             'name': self.name
        #             # 'qty': 1  # Default quantity
                    
        #         }
        #         self.scanner_line_ids = [(0, 0, vals)]
        #     else:
        #         # Jika tidak ditemukan, tampilkan popup dengan pesan
        #         raise UserError('Data tidak ditemukan untuk barcode: %s' % self.barcode)
        #         self.price = 0
        #         self.name = ''
                

        #     # Kosongkan input barcode setelah proses selesai
        #     self.barcode = ''
            

            
    def print_scanner_lines(self):
       
            return self.env.ref('scanning_codabar.action_report_scanner_lines').with_context(
                # grouped_data=grouped_data,
                active_model='scanner.line',
                active_ids=self.scanner_line_ids.ids,
                # grouped_data=grouped_data
            ).report_action(self.scanner_line_ids)
    
class ScannerLine(models.Model):
    _name = 'scanner.line'
    _description = 'Scanner Line'
    
    scanner_id = fields.Many2one('scanner.scanner', string='Scanner Reference' , ondelete='cascade')
    barcode = fields.Char(string='Codabar')
    price = fields.Float(string='Price')
    name = fields.Char(string='Name')
   

   
    
