{
    'name': 'Job Management',
    'version': '1.0.0',
    'category': '',
    'sequence': -500,
    'author': 'Manthan',
    'summary': 'Complete job management system',
    'description': """Complete job management system for all""",
    'depends': ['mail','hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/view_candidate.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
