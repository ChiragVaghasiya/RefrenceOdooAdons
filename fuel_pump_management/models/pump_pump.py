
from odoo import models, fields, api
import ast



class PumpPump(models.Model):
    _name = 'pump.pump'

    def get_product_from_categ(self):
        domain = []
        parent_categ_id = self.env['product.category'].search([('name', 'ilike', 'Fuel')], limit=1)
        if parent_categ_id:
            domain = ['|', ('categ_id', '=', parent_categ_id.id)]
        pos_categ_id = self.env['pos.category'].search([('name', 'ilike', 'Fuel')], limit=1)
        if pos_categ_id:
            domain += [('pos_categ_id', '=', pos_categ_id.id)]
        return domain
    


    name = fields.Char('Name', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    sr_no = fields.Char('Serial No.')
    fuel_type = fields.Many2one('product.product',string='Fuel type', domain=get_product_from_categ)
    pos_config = fields.Many2one('pos.config', 'POS')
    balance_reports = fields.One2many('balance.report', 'pump_id', string='Balance Reports')
    
    
    def action_balancing_report(self):
        action_ref = 'fuel_pump_management.action_balance_report'
        action = self.env['ir.actions.act_window']._for_xml_id(action_ref)
        action['context'] = dict(ast.literal_eval(action.get('context')))
        return action

    
    
    _sql_constraints = [
        ('name_company_uniq', 'unique (name,company_id)', 'The Name must be unique per Company !'),
        ('name_sr_no_uniq', 'unique (sr_no)', 'The Serial Number must be unique per Pump !'),
    ]

