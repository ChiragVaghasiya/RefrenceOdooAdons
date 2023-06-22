from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _



class PakshUpdateState(models.TransientModel):
    _name = 'paksh.update.state'
    _description = 'Change the state of the record'

    state = fields.Selection([
            ('pending', 'Pending'),
            ('rejected', 'Rejected'),
            ('accepted', 'Accepted'),
            ],string="State")


    def update_state(self):
        active_ids = self._context.get('active_ids', []) or []
        for record in self.env[self._context['active_model']].browse(active_ids):
            record.state = self.state


class UpdateState(models.TransientModel):
    _name = 'update.state'
    _description = 'Change the state of the record'

    state = fields.Selection([
            ('pending', 'Pending'),
            ('rejected', 'Rejected'),
            ('accepted', 'Accepted'),
            ],string="State")


    def update_state(self):
        active_ids = self._context.get('active_ids', []) or []
        for record in self.env[self._context['active_model']].browse(active_ids):
            record.state = self.state