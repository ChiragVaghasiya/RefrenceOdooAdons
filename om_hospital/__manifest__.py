{
    "name": "Hospital Management system",
    "application": True,
    "summary": "This appluication for Hospital Managment System.",
    "version": "1.0.0",
    "category": "",
    "website": "www.asjhaskjd/saasg/sjdhj",
    "author": "Chirag Vaghasiya",
    "license": "",
    "installable": True,
    "depends": ['mail','product','account','board'],
    "development_status": "",
    "maintainers": [],
    'demo':[],
    "excludes": [],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/patient_tags_data.xml",   # data ni xml file security pachi anr=e wizard pel aave
        "data/cron.xml",
        "data/patient.tags.csv",        # data ni csv file data xml pachi anr=e wizard pel aave
        "wizard/cancel_appointment.xml",  
        "wizard/mail_to_patient.xml",
        "views/menu.xml",
        "views/patient_view.xml",
        "views/female_patient_view.xml",
        "views/appointment.xml",
        "views/dashbord.xml",
        "views/patient_tags.xml",
        "views/lab.xml",
        "views/odoo_playground.xml",
        "views/res_config_settings_views.xml",
        "reports/report.xml",
        "reports/patient_card.xml",
        "reports/invoice_printing.xml",
        "reports/inherit_patient_card.xml",
        "reports/header&footer.xml",
    ],
    "sequence": -500,
    'license': 'LGPL-3',
}