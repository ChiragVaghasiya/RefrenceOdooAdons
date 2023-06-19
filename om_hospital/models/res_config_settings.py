from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cancel_days = fields.Integer(string = "Cancel Days" , config_parameter ='om_hospital.cancel_days')
    # config_parameter ='om_hospital.cancel_days' --- aa line etla mate lakhi 6 ke , aa data save thay te mate ......   "System Parameters"--aani ander save thase aa field na data.....