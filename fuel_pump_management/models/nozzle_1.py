from odoo import models, fields, api
from lxml import etree



class PumpNozzle(models.Model):
    _name = 'pump.pump.nozzle'

    stage = fields.Selection([('opening', 'Opening'), ('closing', 'Closing')], 'Stage')
    pump_rdgs = fields.Monetary('Pump RDG $', )
    pump_rdgl = fields.Float('Pump RDG L')
    pump_rdg_side = fields.Float('Pump RDG Side')
    
    balance_report_id = fields.Many2one('balance.report')
    company_id = fields.Many2one('res.company', string='Company', related='balance_report_id.company_id', readonly=True)
    currency_id = fields.Many2one('res.currency', related='balance_report_id.currency_id', string="Currency", readonly=True)
    pump_id = fields.Many2one('pump.pump', string='Pump')
    session_id = fields.Many2one('pos.session', string='Session', related='balance_report_id.pos_session')
    config_id = fields.Many2one('pos.config', string='PoS Config', related='session_id.config_id')
    
