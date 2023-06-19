{
    'name': 'Dashboard',
    'version': '1.0',
    'author' : 'Helmi Dhaoui',
    'website' : 'http://globalservicescompany.net',
    'category': 'Management',
    'depends': ['base','om_hospital'],
    "application": True,
    'data': [
        'data/dashboard_data.xml',
        'security/dashboard_security.xml',
        'security/ir.model.access.csv',
        'views/dashboard_view.xml',
        'views/res_config_view.xml',
        # 'views/assets.xml',
    ],
    'assets': {
    'web.assets_backend': [

        'dashboard/static/src/css/dashboard.css',
        'dashboard/static/src/css/menual.css',
        'dashboard/static/src/css/font-awesome.css',
        'dashboard/static/src/css/simple-iconpicker.min.css',
        'dashboard/static/src/js/menual.js',
        'dashboard/static/src/js/raphael.js',
        'dashboard/static/src/js/raphael.min.js',

    ]},
    'installable': True,
    'images': ['static/description/logo.png'],
    'live_test_url': 'https://www.youtube.com/embed/v1wx9yJFpHA',
    "sequence" : -10,

}
