from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Tharav(models.Model):
    _name = 'tharav.model'
    _description = 'Tharav'
    _rec_name = 'tharav_subject_and_id'

    @api.onchange('tharav_id', 'subject', 'start_date', 'tags_id')
    def _get_self_id(self):

        if self.id != False:
            if self.id.origin != False or self.id.origin != None:
                self.self_id2 = True

    @api.onchange('tharav_id', 'subject')
    def _get_tharav_subject_id(self):
        lists = [False, None]
        for rec in self:
            if rec.subject not in lists and rec.tharav_id not in lists:
                rec.tharav_subject_and_id = rec.tharav_id + " - " + rec.subject

    @api.constrains('subject')
    def _check_subject(self):
        if self.subject != False and self.subject != None:
            if len(self.subject) > 3000:
                raise ValidationError("Subject should must be of 3000 character Max.")
    
    @api.constrains('description')
    def _check_description(self):
        if self.description != False and self.description != None:
            if len(self.description) > 10000:
                raise ValidationError("Description should must be of 10000 character Max.")

    tharav_subject_and_id = fields.Char("Id- Subject", compute=_get_tharav_subject_id)
    tharav_id = fields.Char("Tharav", required=True)
    subject = fields.Text("Subject", required=True)
    paksh_id = fields.Many2one('paksh.model', "Paksh", required=True)
    start_date = fields.Date("Start Date", required=True)
    discontinue_date = fields.Date("Discontinue Date")
    manage_history = fields.Boolean("Manage History")
    tags_id = fields.Many2many('lekh.tags.model', string="Tags", required=True)
    description = fields.Text("Description")
    self_id = fields.Char("ID", default=_get_self_id)
    self_id2 = fields.Boolean("ID2", default=False)
    color = fields.Integer("")
    ref_id = fields.Integer("")

    def unlink(self):

        for rec in self:

            relations = ""
            LekhObj = self.env['lekh.model'].search([('tharav.id', '=', rec.id)])
            if LekhObj:
                relations += "Lekh, "

            NirnaamiLekhObj = self.env['nirnaami.lekh.model'].search([('tharav.id', '=', rec.id)])
            if NirnaamiLekhObj:
                relations += "Nirnaami Lekh, "

            VideoObj = self.env['video.model'].search([('tharav_id.id', '=', rec.id)])
            if VideoObj:
                relations += "Video, "

            BookObj = self.env['book.model'].search([('tharav_id.id', '=', rec.id)])
            if BookObj:
                relations += "Book, "

            if relations != "":
                raise ValidationError("You can not delete these record it has relation with " + relations + "model.")

        return super(Tharav, self).unlink()
