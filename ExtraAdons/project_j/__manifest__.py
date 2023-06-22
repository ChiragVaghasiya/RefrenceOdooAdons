# -*- coding: utf-8 -*-
{
    'name': "Project J",

    'summary': """
        This Application is under Development. """,

    'description': """
       Test
    """,

    'author': "Aspire Softserv Pvt. Ltd.",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'web'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'mail/mail_templates.xml',
        'wizards/wizards_view.xml',
        'wizards/advance_search_view.xml',
        'wizards/multiple_records_wiz_view.xml',
        'views/global_social_info_view.xml',
        'views/mahatma_view.xml',
        'views/samuday_view.xml',
        'views/lekh_view.xml',
        'views/lekh_related_info_view.xml',
        'views/person_view.xml',
        'views/sanstha_view.xml',
        'views/paksh_view.xml',
        'views/magazine_view.xml',
        'views/tharav_view.xml',
        'views/nirnaami_lekh_view.xml',
        'views/book_view.xml',
        'views/samiti_view.xml',
        'views/videos_view.xml',
        'views/config_tables_view.xml',
        'views/documents_view.xml',
        'views/users_view.xml',
        'views/magazine_ank_view.xml',
        'views/project_j_scheduler_view.xml',
        'views/documents_reference_type_view.xml',
        'views/advance_search_results_view.xml',
        'views/mail_chatter_notifications.xml',
        'views/project_j.xml',
        
        'views/subject.xml',
        'views/main_menu.xml',
    ],
    # only loaded in demonstration mode

    'installabble': True,
}
