from odoo import models, fields, api


class Nozzle2(models.Model):
    _name = 'nozzle.2'

    stage = fields.Selection([('opening', 'Opening'), ('closing', 'Closing')], 'Stage', ondelete="set null")
    pump_rdgs = fields.Char('Pump RDG S')
    pump_rdgl = fields.Char('Pump RDG L')
    pump_rdg_side = fields.Char('Pump RDG Side')
    
    balance_report_id = fields.Many2one('balance.report')
    