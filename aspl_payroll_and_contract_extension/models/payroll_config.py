from odoo import models, fields, api, _

class new_payroll_config(models.Model):
    _inherit = 'hr.salary.rule'

    taxable = fields.Boolean(string="Taxable")
    appear_on_contract = fields.Boolean(string="Appear on Contract")

    

