# -*- coding: utf-8 -*-

{
    'name': "Highcharts",
    'version': '11.0.1.0.0',
    'summary': """ Dynamic Dashboard Module
    """,
    'description': """
    """,
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://www.candidroot.com/",
    'category': 'Tools',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/dashboard_export_wizard_view.xml',
        'wizard/import_dashboard_wizard_view.xml',
        # 'views/assets.xml',
        'views/highchart_dashboard_views.xml',
        'views/highchart_dashboard_chart_views.xml',
        'views/menuitem.xml',
    ],
    'demo': [
        'demo/dashboard_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'highchart_dashboard/static/src/css/highchart_dashboard.css',
            'highchart_dashboard/static/src/less/highchart_dashboard.less',
            'highchart_dashboard/static/src/js/dashboard_chart_preview.js',
            'highchart_dashboard/static/src/js/highchart_dashboard.js',
            'highchart_dashboard/static/src/js/icon_view_widget.js',
            'highchart_dashboard/static/src/js/list_controller.js',
            'highchart_dashboard/static/src/js/field_domain.js',
        ],
    'web.assets_qweb': [
            'highchart_dashboard/static/src/xml/base_import.xml',
            'highchart_dashboard/static/src/xml/highchart_templates.xml',
            'highchart_dashboard/static/src/xml/icon_view_widget.xml',
            'highchart_dashboard/static/src/xml/tile_templates.xml',
        ],
    },
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': False
}
