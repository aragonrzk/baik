{
    'name': "Scanning Line Report",
    'version': '17.0.1.0.0',
    'category': 'custom',
    'summary': "Scanning Line Report",
    'description': """
        This module adds reporting capabilities for scanner line data.
        Features:
        - List view of all scanner line entries
        - Totals and analysis
    """,
    'depends': ['scanning_codabar','purchase'],
    'data': [
        'views/scanner_line_report_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}