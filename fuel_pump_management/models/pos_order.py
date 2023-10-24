# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = "pos.order"

    nozzle_id = fields.Many2one('pump.pump.nozzles', help="From Which Nozzle Fuel goes out", states={'done': [('readonly', True)], 'invoiced': [('readonly', True)]})

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['nozzle_id'] = ui_order.get('nozzle_id')
        return order_fields

    def _export_for_ui(self, order):
        result = super(PosOrder, self)._export_for_ui(order)
        result.update({
            'nozzle_id': order.nozzle_id.id,
        })
        return result
