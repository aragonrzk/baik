{
    'name': 'Scanning Codabar',
    'version': '1.0',
    'summary': 'Module for scanning Codabar barcodes and QR codes',
    'category': 'Custom',
    'author': 'HantuRimba',
    'website': 'http://yourwebsite.com',
    'depends': ['base', 'purchase'],
    'data': [
        'views/scanner_views.xml',
        'security/ir.model.access.csv',
        'reports/scanner_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
