from odoo import models, fields, api
from odoo.exceptions import ValidationError, Warning


class Documents(models.Model):
    _name = 'documents.model'
    _description = 'Documents'
    _rec_name = 'subject'

    def _get_tags(self):
        for rec in self:
            result = ""
            if rec.tags_id != False and rec.tags_id != None:
                if len(rec.tags_id) > 0:
                    for tag in rec.tags_id:
                        result += tag.lekh_tag_name + ", "
            rec.tags_copy = result

    def _get_tharav(self):
        for rec in self:
            result = ""
            if rec.tharav_id != False and rec.tharav_id != None:
                if len(rec.tharav_id) > 0:
                    for tharav in rec.tharav_id:
                        result += tharav.tharav_subject_and_id + ", "
            rec.tharav_copy = result

    doc_type = fields.Selection(
        [('lekh', 'Lekh'), ('nirnaami_lekh', 'Nirnaami Lekh'), ('book', 'Book'), ('video', 'Video')], required=True,
        readonly=True)

    sr_no = fields.Integer("Sr. No.", readonly=True)
    sr_no_prefix = fields.Char("Sr. No. With Prefix", readonly=True)
    subject = fields.Char("Subject", readonly=True)
    tags_id = fields.Many2many('lekh.tags.model', string="Tags", readonly=True)
    tharav_id = fields.Many2many('tharav.model', string="Tharav", readonly=True)
    description = fields.Text("Description", readonly=True)
    remark = fields.Text("Remark", readonly=True)
    star_rating = fields.Selection([('one', 'One'), ('two', 'Two'), ('three', 'Three'), ('four', 'Four')],
                                   "Star Ratings for Importance Of Utility", readonly=True)

    lekh_ids = fields.One2many('lekh.model', 'lekh_ref_field', string="Lekh", readonly=True)
    book_ids = fields.One2many('book.model', 'book_ref_field', string="Book", readonly=True)
    video_ids = fields.One2many('video.model', 'video_ref_field', string="Video", readonly=True)
    nirnaami_lekh_ids = fields.One2many('nirnaami.lekh.model', 'nirnaami_lekh_ref_field', string="Nirnaami Lekh",
                                        readonly=True)

    doc_related_info_lines = fields.One2many('documents.related.info', 'docs_related_info_id', "Related Info lines",
                                             readonly=True)
    doc_global_related_info = fields.One2many('global.related.info', 'ref_field', string="Doc Related Info.")

    doc_ref_field = fields.Integer("Ref. Id.")
    color = fields.Integer("")
    tags_copy = fields.Char("Tags", compute=_get_tags)
    tharav_copy = fields.Char("Tharav", compute=_get_tharav)
    related_info = fields.Char("Related Info.", readonly=True)
    can_delete = fields.Boolean("Delete", readonly=True)
    ref_field = fields.Integer("")
    results = fields.Many2one('advance.search.results.model', string="Results")

    @api.model
    def create(self, values):

        lists = []
        if 'related_info' in values:
            if values['related_info'] != False and values['related_info'] != None and len(values['related_info']) > 0:
                for rec in values['related_info']:

                    samuday_ids = False
                    if rec[7] != False and rec[7] != None and len(rec[7]) > 0:
                        MahatmaObj = self.env['mahatma.model'].search([('id', 'in', rec[7])])
                        if len(MahatmaObj) > 0:
                            samuday_ids = []
                            for a in MahatmaObj:
                                if a.samuday_id.id != False and a.samuday_id.id != None:
                                    samuday_ids.append(a.samuday_id.id)

                    lists.append((0, 0,
                                  {'date_of_publishing': rec[0], 'date_of_occurance': rec[1], 'vikram_samvat': rec[2],
                                   'category': rec[3], 'reference_type': rec[4],
                                   'person_id': rec[5], 'sanstha_id': rec[6], 'mahatma_id': rec[7],
                                   'samuday_id': samuday_ids, 'samiti_id': rec[8]}))

            values['doc_related_info_lines'] = lists

        record = super(Documents, self).create(values)

        return record

    def write(self, vals):
        res = super(Documents, self).write(vals)
        return res

    def unlink(self):

        for rec in self:

            if rec.can_delete == False:
                raise ValidationError("You can not delete any documents from here.")
            else:
                return super(Documents, self).unlink()

    # def fields_get(self, fields=None):
    #     fields_to_hide = ['related_info', 'doc_related_info_lines', 'lekh_ids', 'book_ids', 'video_ids',
    #                       'nirnaami_lekh_ids', 'doc_ref_field', 'color', 'tags_copy', 'tharav_copy']
    #     res = super(Documents, self).fields_get()
    #     for field in fields_to_hide:
    #         res[field]['selectable'] = False
    #     return res


class DocumentsRelatedInfo(models.Model):
    _name = 'documents.related.info'
    _description = 'Documents Related Info'

    date_of_publishing = fields.Date("Date Of Publishing")
    date_of_occurance = fields.Date("Date Of Occurance")
    vikram_samvat = fields.Char("Vikram Samvat Of Publishing")
    category = fields.Selection([('original', 'Original Documents'), ('photo_copy', 'Photo Copy Or Xeroxx'),
                                 ('partial', 'Partial Documents (With No Reference)'), ('high', 'High'),
                                 ('low', 'Low')], "Category", readonly=True)
    docs_related_info_id = fields.Integer("ID")
    person_id = fields.Many2many('person.model', string="Person", required=True)
    sanstha_id = fields.Many2many('sanstha.model', string="Sanstha", required=True)
    mahatma_id = fields.Many2many('mahatma.model', string="Mahatma", required=True)
    samuday_id = fields.Many2many('samuday.model', string="Samuday", required=True)
    samiti_id = fields.Many2many('samiti.model', string="Samiti", required=True)
    reference_type = fields.Many2one('documents.reference.type',string="Reference Type")
