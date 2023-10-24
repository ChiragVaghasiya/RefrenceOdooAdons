from odoo import models, fields, api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    def get_warehouse_from_company(self):
        domain = []
        if self.nozzle_company:
            domain = [('company_id', '=', self.nozzle_company.id)]
        return domain

    is_nozzle_used = fields.Boolean('Is Nozzle Used')

    nozzle_company = fields.Many2one('res.company', string='Nozzle Company Set')
    nozzle_warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse for Nozzle Products', domain=get_warehouse_from_company)
    pump_ids = fields.One2many('pump.pump', 'pos_config', string='Nozzle Pumps Used')

    def check_products_in_category(self, category, warehouse_id, session_id):
        if category and self.is_nozzle_used and self.company_id == self.nozzle_company:
            print ('ffff', category)
            categ_id = category.get('id')
            products = self.env['product.product'].search([('categ_id', '=', categ_id)])
            nozzle_products = self.env['pump.pump'].search([('pos_config', '=', self.id)]).mapped('fuel_type')
            warehouse_id = warehouse_id[0]
            for product in products:
                if product in nozzle_products:
                    product_start = self.env['product.session.start'].sudo().create({'product_id': product.id, 'warehouse_id': warehouse_id, 'session_id': session_id})
                    print ('FFFFFFFF', product_start)
        return True

    