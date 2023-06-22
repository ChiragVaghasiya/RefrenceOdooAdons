from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LekhReference(models.Model):
    _name = 'lekh.reference.model'
    _description = 'Lekh Reference'
    _rec_name = 'reference_name'

    reference_name = fields.Char("Name", required=True)
    type_of_reference = fields.Selection([('news_paper', 'News Paper'), ('magazine', 'Magazine'), ('book', 'Book'),
                                          ('invitation_letter', 'Invitation Letter'),
                                          ('general_letter', 'General Letter'), ('letter', 'Letter'),
                                          ('pamphlet', 'Pamphlet'), ('website', 'Website'), ('others', 'Others')],
                                         "Type", required=True)


class LekhRelatedInfo(models.Model):
    _name = 'lekh.related.info.model'
    _description = 'Lekh Related Info'
    _rec_name = 'news_heading'

    @api.onchange('reference_type')
    def _get_reference_domain(self):
        if self.reference_type != False and self.reference_type != None:
            res = {}
            res['domain'] = {'reference': [('type_of_reference', '=', self.reference_type)]}
            return res
        else:
            pass

    @api.onchange('reference_type')
    def reset_reference(self):
        self.reference = False

    @api.onchange('mahatma_id')
    def _get_paksh(self):
        for rec in self:
            paksh_ids = []
            if rec.mahatma_id != None and rec.mahatma_id != False:
                if len(rec.mahatma_id) > 0:
                    for mahatma in rec.mahatma_id:
                        if mahatma.id != None and mahatma.id != False:
                            if mahatma.paksh_id.id != False and mahatma.paksh_id.id != None:
                                if mahatma.paksh_id.id not in paksh_ids:
                                    paksh_ids.append(mahatma.paksh_id.id)

            if len(paksh_ids) > 0:
                rec.paksh_id = paksh_ids
            else:
                rec.paksh_id = False

    @api.onchange('mahatma_id')
    def _get_samuday(self):
        for rec in self:
            samuday_ids = []
            if rec.mahatma_id != None and rec.mahatma_id != False:
                if len(rec.mahatma_id) > 0:
                    for mahatma in rec.mahatma_id:
                        if mahatma.id != None and mahatma.id != False:
                            if mahatma.samuday_id.id != False and mahatma.samuday_id.id != None:
                                if mahatma.samuday_id.id not in samuday_ids:
                                    samuday_ids.append(mahatma.samuday_id.id)

            if len(samuday_ids) > 0:
                rec.samuday_id = samuday_ids
            else:
                rec.samuday_id = False

    lekh_related_id = fields.Integer("ID")
    news_heading = fields.Text("News Heading")
    vikram_samvant_of_publishing = fields.Char("Vikram Samvant Of Publishing")
    samvat_of_occurance = fields.Char("Samvat Of Occurance")
    category = fields.Selection([('original', 'Original Documents'), ('photo_copy', 'Photo Copy OR Xerox'),
                                 ('partial', 'Partial Documents (With no reference)')], "Category", required=True)
    reference_type = fields.Many2one('documents.reference.type',string="Reference Type")

    reference = fields.Many2one('lekh.reference.model', "Reference")
    magazine_reference = fields.Many2one('magazine.model', "Reference Magazine")
    occasion_location = fields.Char("Occasion Location")
    date_of_publishing = fields.Date("Date Of Publishing")
    date_of_occurance = fields.Date("Date Of Occurrence")
    # ank_id = fields.Many2one('ank.model', "Ank")
    # library = fields.Integer("Library")
    page = fields.Char("Page")
    copy = fields.Integer("Copy")

    samiti_id = fields.Many2many('samiti.model', string="Samiti")
    mahatma_id = fields.Many2many('mahatma.model', string="Mahatma")
    person_id = fields.Many2many('person.model', string="Person")
    sanstha_id = fields.Many2many('sanstha.model', string="Sanstha")
    paksh_id = fields.Many2many('paksh.model', string="Paksh")

    lekh_image = fields.Many2many(comodel_name="ir.attachment",
                                  relation="m2m_ir_lekh_image_rel",
                                  column1="m2m_id",
                                  column2="attachment_id",
                                  string="Lekh Image",
                                  attachment=True)
    reference_image = fields.Many2many(comodel_name="ir.attachment",
                                       relation="m2m_ir_reference_image_rel",
                                       column1="m2m_id",
                                       column2="attachment_id",
                                       string="Reference Image",
                                       attachment=True)

    test_images = fields.Many2many(comodel_name='ir.attachment',
                                   string="Attachments", )

    ank = fields.Char("Ank")
    library_field = fields.Char("Library")
    reference_location = fields.Char("Reference Location")
    other_reference_type = fields.Char("Other Reference")
    samuday_id = fields.Many2many('samuday.model', string="Samuday", compute=_get_samuday)

    # field_name = fields.Many2many('res.partner', string="4")

    @api.constrains('news_heading')
    def _check_news_heading(self):
        for rec in self:
            if rec.news_heading != False and rec.news_heading != None:
                if len(rec.news_heading) > 250:
                    raise ValidationError("News Heading should must be of 250 character Max.")

    @api.constrains('vikram_samvant_of_publishing')
    def _check_vikram_samvant_of_publishing(self):
        for rec in self:
            if rec.vikram_samvant_of_publishing != False and rec.vikram_samvant_of_publishing != None:
                if len(rec.vikram_samvant_of_publishing) > 75:
                    raise ValidationError("Vikram Samvant Of Publishing should must be of 75 character Max.")

    @api.constrains('samvat_of_occurance')
    def _check_samvat_of_occurance(self):
        for rec in self:
            if rec.samvat_of_occurance != False and rec.samvat_of_occurance != None:
                if len(rec.samvat_of_occurance) > 75:
                    raise ValidationError("Samvat Of Occurance should must be of 75 character Max.")

    # @api.constrains('copy')
    # def _check_copy(self):
    #     if self.copy != False and self.copy != None:
    #         if len(str(self.copy)) > 11:
    #             raise ValidationError("Copy Of Occurance should must be of 11 character Max.")

    @api.constrains('page')
    def _check_page(self):
        for rec in self:
            if rec.page != False and rec.page != None:
                if len(rec.page) > 75:
                    raise ValidationError("page should must be of 75 character Max.")
