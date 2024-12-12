# -*- coding: utf-8 -*-
###############################################################################
#
# Fortutech IMS Pvt. Ltd.
# Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
{
    'name': 'Report Subtotal Per Page',
    'category': 'Report',
    'summary': 'Report Subtotal Per Page',
    'version': '15.0.1.0.0',
    'license': 'OPL-1',
    'description': """ Total in every report pages.""",
    'depends': ['base', 'sale_management', 'purchase', 'account'],
    'author': "Fortutech IMS Pvt. Ltd.",
    'website': "http://www.fortutechims.com",
    'data': [
        'views/report_invoice_template.xml',
        'views/res_config_settings_view.xml',
        'views/sale_report_templates.xml',
        'views/purchase_order_templates.xml',
    ],
    "price": 19.0,
    "currency": "USD",
    "installable": True,
    "application": True,
    "auto_install": False,
    "images": ['static/description/banner.png'],
}
