from odoo import models, fields, api

class subjectlist(models.Model):
    _name = 'subject.model'
    _description = 'Subjects'

    level = fields.Integer(string="Level")
    name = fields.Char(string="Name")
    parent_id = fields.Many2one('subject.model',string="Parent")




