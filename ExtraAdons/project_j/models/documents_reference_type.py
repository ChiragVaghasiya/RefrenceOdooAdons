from odoo import models, fields, api


class DocumentsReferenceType(models.Model):
    _name = 'documents.reference.type'
    _description = 'Documents Reference Type'
    _rec_name = 'name'

    name = fields.Char("Reference Name")
