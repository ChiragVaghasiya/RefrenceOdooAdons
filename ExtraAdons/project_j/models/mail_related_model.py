from odoo import models, fields, api


class MailRelatedModel(models.Model):
    _name = 'mail.related.model'
    _description = 'Mail Related Model'
    # _rec_name = 'scheduler_name'

    ref_field = fields.Integer("")
    magazine_ank_ids = fields.One2many('magazine.ank', 'ref_field', string="Magazine Ank")
    fix_email = fields.Char("", default="sagar.panchal@aspiresoftserv.com")
    email = fields.Char("", default="sempanchal123@gmail.com")
