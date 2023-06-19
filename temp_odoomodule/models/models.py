from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirned_ser_id = fields.Many2one('res.users',string = "NAME")

    def action_confirm(self):  #  Fuction Inherite Karva mate ...
        print("*******Created Function*********")

        # super(Class_name,self).Function_je_run_karravvu_hoy_te(Argurs_run-karravvu_6_te_func_na)
        super(SaleOrder,self).action_confirm()

        self.confirned_ser_id = self.env.user