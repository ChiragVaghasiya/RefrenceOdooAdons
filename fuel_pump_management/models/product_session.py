from odoo import models, fields, api


class ProductSessionStart(models.Model):
    _name = 'product.session.start'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    session_id = fields.Many2one('pos.session', string='Session')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    qty_availablae = fields.Float('Qty Available on Session Start', compute='compute_qty_available', store=True)

    @api.depends('warehouse_id')
    def compute_qty_available(self):
        for product_start in self:
            product_start.qty_availablae = 0.0
            if product_start.warehouse_id:
                product_start.qty_availablae = product_start.product_id.with_context(
                    warehouse=self.warehouse_id.id, fuel_pump=True).qty_available


class ProductProduct(models.Model):
    _inherit = 'product.product'


    def _get_domain_locations(self):
        
        Warehouse = self.env['stock.warehouse']
        def _search_ids(model, values):
            ids = set()
            domain = []
            for item in values:
                if isinstance(item, int):
                    ids.add(item)
                else:
                    domain = expression.OR([[('name', 'ilike', item)], domain])
            if domain:
                ids |= set(self.env[model].search(domain).ids)
            return ids

        # We may receive a location or warehouse from the context, either by explicit
        # python code or by the use of dummy fields in the search view.
        # Normalize them into a list.
        location = self.env.context.get('location')
        if location and not isinstance(location, list):
            location = [location]
        warehouse = self.env.context.get('warehouse')
        fuel_pump = self.env.context.get('fuel_pump')
        if warehouse and not isinstance(warehouse, list):
            warehouse = [warehouse]
        # filter by location and/or warehouse
        if warehouse:
            w_ids = set(Warehouse.browse(_search_ids('stock.warehouse', warehouse)).mapped('view_location_id').ids)
            if fuel_pump:
                f_ids = set(Warehouse.browse(_search_ids('stock.warehouse', warehouse)).mapped('lot_stock_id').ids)
                w_ids = w_ids | f_ids
            if location:
                l_ids = _search_ids('stock.location', location)
                location_ids = w_ids & l_ids
            else:
                location_ids = w_ids
        else:
            if location:
                location_ids = _search_ids('stock.location', location)
            else:
                location_ids = set(Warehouse.search([]).mapped('view_location_id').ids)
        return self._get_domain_locations_new(location_ids, compute_child=self.env.context.get('compute_child', True))


    