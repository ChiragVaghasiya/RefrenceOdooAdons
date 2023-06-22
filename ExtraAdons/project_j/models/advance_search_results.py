from odoo import models, fields, api


class AdvanceSearchResults(models.Model):
    _name = 'advance.search.results.model'
    _description = 'Advance Search Result'
    _rec_name = 'name'

    def _get_results_count(self):
        elements = [None, False]
        for rec in self:
            if rec.result_type == 'doc':
                if rec.doc_ids not in elements and len(rec.doc_ids) > 0:
                    rec.results_count = len(rec.doc_ids)
                else:
                    rec.results_count = False

            elif rec.result_type == 'magazine':
                if rec.magazine_ids not in elements and len(rec.magazine_ids) > 0:
                    rec.results_count = len(rec.magazine_ids)
                else:
                    rec.results_count = False

            else:
                rec.results_count = False

    def pass_method(self):
        pass

    ref_field = fields.Integer("")
    name = fields.Char("Name")
    result_type = fields.Selection([('doc', 'Documents'), ('magazine', 'Magazine')], string="Type", readonly=True)
    doc_ids = fields.Many2many('documents.model', string="Documents")
    magazine_ids = fields.One2many('magazine.model', 'ref_id', string="Magazine")
    results_count = fields.Integer("Records", compute=_get_results_count)
