# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    line_per_page = fields.Integer()

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            line_per_page=int(self.env['ir.config_parameter'].sudo().get_param('fims_report_subtotal_per_page.line_per_page'),))
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        lines = self.line_per_page
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('fims_report_subtotal_per_page.line_per_page', lines)
