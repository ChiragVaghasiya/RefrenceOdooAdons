# -*- coding: utf-8 -*-

{
    "name": "Product Extension",
    "summary": "Product template adjustment",
    "version": "17.0.0.1.0",
    "license": "AGPL-3",
    "description": """This module introduces functionality to convert product template into product variant.""",
    "website": "",
    "depends": [
        "product",
        "stock"
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'wizards/product_merge_view.xml',
        'wizards/product_product_merge_view.xml',
        'wizards/product_template_update_view.xml',
        'wizards/custom_import_model.xml',
        'reports/print_labels.xml'
    ],
    'assets': {
        'web.assets_backend': [
            "product_extension/static/src/js/import_records.js",
            "product_extension/static/src/js/import_records.xml",
        ],
    },
    "application": True,
    "installable": True,
}
