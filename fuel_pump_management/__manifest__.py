
{
    'name': 'Fuel Pump Management',
    'category': 'Project',
    'version': '15.0.0.0',
    'summary': 'Fuel Pump Management',
    'depends': ['base', 'stock', 'point_of_sale', 'pos_sale'],
    'description': """ Fuel Pump Management """,
    'data':[
                'security/sales_team_security.xml',
                'security/ir.model.access.csv',
                'report/balance_report.xml',
                'report/balance_report_template.xml',
                'report/report_nozzle_readings.xml',
                # 'views/pos_assets.xml',
                'views/assets.xml',
                'views/pump_pump.xml',
                'views/balance_report.xml',
                'views/nozzle_1.xml',
                'views/pos_session.xml',
                'views/pos_config_views.xml',
                'wizard/nozzle_reading_view.xml',
                # 'views/res_users_view.xml',
                'data/fuel_data.xml',
            ],
    # 'assets': {
    #     'point_of_sale.assets': [
    #         'fuel_pump_management/static/src/js/models.js',
    #     ],

    # },
    'qweb': [
            'static/src/xml/Nozzlename.xml',
            'static/src/xml/chrome.xml',
            ],
    'demo': [ ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application' :  False,
    "images":[ ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
