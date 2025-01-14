# source venv/bin/activate
# mainkan di localhost:807
# python3.12 odoo-bin -c debian/odoo.conf
# ./odoo-bin -c debian/odoo.conf -d odoo_17 -u modul_custom -- untuk updatenya modul nya
# python3.12 odoo-bin -c debian/odoo.conf --log-level=debug --log-handler=*:DEBUG --dev=all
# tail -f /var/log/odoo/odoo.log
{
    'name': 'Barcode and QR Code Generator',
    'version': '17.0.1.0.0',
    'category': 'Tools',
    'summary': 'Generate Barcodes and QR Codes based on date range',
    'sequence': 1,
    'author': 'Arie',
    'website': 'https://www.yourwebsite.com',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/barcode_generator_views.xml',
        'reports/report_barcode_template.xml',
        'reports/barcode_reports.xml',
    ],
    'assets': {
            'web.assets_backend': [
            'barcode_generator/static/src/js/barcode_generator_form.js',
            'barcode_generator/static/src/scss/barcode_form.scss',
            ],
        },
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['qrcode', 'python-barcode'],
    },
}