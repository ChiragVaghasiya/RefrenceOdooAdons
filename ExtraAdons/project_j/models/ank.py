from odoo import models, fields, api


class Ank(models.Model):
    _name = 'ank.model'
    _description = 'Ank'
    _rec_name = 'ank_name'

    ank_name = fields.Char("Name")
