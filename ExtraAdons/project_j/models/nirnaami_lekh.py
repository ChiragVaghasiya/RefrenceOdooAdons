from odoo import models, fields, api
from odoo.exceptions import ValidationError
from openerp.tools.translate import _


class NirnaamiLekh(models.Model):
    _name = 'nirnaami.lekh.model'
    _description = 'Nirnaami Lekh'
    _rec_name = 'nirnaami_lekh_sr_no'

    def check_duplicate_records(self):

        if self.id != None and self.id != False:
            NirnaamiLekhSearchObj = self.env['nirnaami.lekh.model'].search([])

            if len(NirnaamiLekhSearchObj) > 0:
                msg = str(len(NirnaamiLekhSearchObj)) + " matching records found."
                nirnaami_lekh_rec = NirnaamiLekhSearchObj
                flag = True
            else:
                msg = "No matching record Found."
                nirnaami_lekh_rec = False
                flag = False

            message_id = self.env['message.wizard'].create(
                {'message': msg, 'nirnaami_lekh_id': nirnaami_lekh_rec, 'display_flag': flag,
                 'display_model': 'nirnaami_lekh'})
            return {
                'name': _('Duplicate Search Result'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'message.wizard',
                'res_id': message_id.id,
                'target': 'new'
            }

    @api.onchange('tharav', 'tags_id', 'status', 'remark', 'subject', 'nirnaami_lekh_related_info_lines', 'total_page')
    def _get_self_id(self):

        for rec in self:
            if rec.id != False:
                if rec.id.origin != False and rec.id.origin != None:
                    rec.nirnaami_lekh_self_id2 = True

    @api.onchange('nirnaami_lekh_sr_no')
    def _get_display_sr_no(self):
        for rec in self:
            if rec.nirnaami_lekh_sr_no != False and rec.nirnaami_lekh_sr_no != None:
                rec.nirnaami_lekh_display_sr_no = "N" + str(rec.nirnaami_lekh_sr_no)

    def _get_current_id(self):
        self.current_id = self.id
        DocumentObj = self.env['documents.model'].search([('id', '=', self.doc_ref)])
        if DocumentObj:
            DocumentObj.nirnaami_lekh_ids = (4, self.current_id)

    @api.onchange('nirnaami_lekh_related_info_lines')
    def _get_tharav_domain(self):
        paksh_ids = []
        if self.nirnaami_lekh_related_info_lines != False and self.nirnaami_lekh_related_info_lines != None and len(
                self.nirnaami_lekh_related_info_lines) > 0:

            for related_info_line in self.nirnaami_lekh_related_info_lines:

                if related_info_line.paksh_id != False and related_info_line.paksh_id != None and len(
                        related_info_line.paksh_id) > 0:

                    for paksh in related_info_line.paksh_id:
                        paksh_ids.append(paksh._origin.id)

            if len(paksh_ids) > 0:
                return {'domain': {'tharav': [('paksh_id.id', 'in', paksh_ids)]}}
            else:
                pass

    # nanami_lekh_name = fields.Char("Name")
    nirnaami_lekh_sr_no = fields.Integer("Sr. No.")
    nirnaami_lekh_display_sr_no = fields.Char("Sr. No.", compute='_get_display_sr_no', store=True, readonly=True)
    subject = fields.Char("Subject")
    tags_id = fields.Many2many('lekh.tags.model', string="Tags")
    # status = fields.Selection([('approved','Approved'), ('pending','Pending'), ('rejected','Rejected')], "Status")
    description = fields.Text("Description")

    nirnaami_lekh_related_info_lines = fields.One2many('nirnaami.lekh.related.info.model',
                                                       'nirnaami_lekh_related_info_id', "Related Info", required=True)

    tharav = fields.Many2many('tharav.model', string="Tharav")
    total_page = fields.Char("Total Page", required=True)
    copy = fields.Integer("Copy")
    # link_with_field = fields.Many2many(, "Link With Field")
    link_with_field = fields.Many2many('documents.model', string="Link With Field")
    # link_with_field = fields.Char("Link With Field")
    remark = fields.Text("Remark")
    star_rating = fields.Selection([('one', 'One'), ('two', 'Two'), ('three', 'Three'), ('four', 'Four')], "Rating")

    nirnaami_lekh_news_heading_copy = fields.Char("News Heading")
    nirnaami_lekh_person_copy = fields.Char("Person")
    nirnaami_lekh_sanstha_copy = fields.Char("Sanstha")
    nirnaami_lekh_mahatma_copy = fields.Char("Mahatma")
    paksh_copy = fields.Char("Paksh")
    nirnaami_lekh_self_id2 = fields.Boolean("ID2", default=False)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ], string="Actions", default='pending')

    nirnaami_lekh_ref_field = fields.Integer("Nirnaami Lekh Ref.")
    rec_state = fields.Selection([('draft', 'Draft'), ('created', 'Created')], default='draft')
    doc_ref = fields.Integer("Doc. Id.")
    current_id = fields.Integer(compute=_get_current_id)
    nirnaami_lekh_global_related_info = fields.One2many('global.related.info', 'ref_field',
                                                        string="Nirnaami Lekh Related Info.")

    def accept_video(self):
        self.write({
            'state': 'accepted',
        })

    def reject_video(self):
        self.write({
            'state': 'rejected',
        })

    @api.constrains('nirnaami_lekh_related_info_lines')
    def _check_nirnaami_lekh_related_info_lines(self):
        if len(self.nirnaami_lekh_related_info_lines) > 0:
            pass
        else:
            raise ValidationError("Please inseret related Info")

    # @api.constrains('total_page')
    # def _check_total_page(self):
    #     if self.total_page <= 0:
    #         raise ValidationError("Please enter 'Total Page' correctly")

    @api.model
    def create(self, values):

        if 'nirnaami_lekh_related_info_lines' not in values:
            raise ValidationError("Please inseret related Info")

        lists = []
        try:
            NirnaamiLekhObj = self.env['nirnaami.lekh.model'].search([('id', '!=', self.id)])
        except:
            NirnaamiLekhObj = self.env['nirnaami.lekh.model'].search([])
        if NirnaamiLekhObj:
            for rec in NirnaamiLekhObj:
                lists.append(rec.nirnaami_lekh_sr_no)

        lists.sort()
        last_element = 0
        zero_count = 0
        result = None
        for data in lists:
            if data == 0 and zero_count < 1:
                zero_count += 1
                continue
            elif (data - 1) != last_element:
                result = last_element + 1
                break
            last_element = data

        if values['nirnaami_lekh_sr_no'] > 0:
            if values['nirnaami_lekh_sr_no'] in lists:
                if result == None:
                    raise ValidationError("Sr.No. " + str(
                        values['nirnaami_lekh_sr_no']) + " is already taken, You can use any value greater than " + str(
                        lists[-1]) + ".")

                else:
                    raise ValidationError(
                        "Sr.No. " + str(values['nirnaami_lekh_sr_no']) + " is already taken, You can use '" + str(
                            result) + "' or any value greater than " + str(lists[-1]) + ".")

        else:
            if len(lists) > 0:
                if result == None:
                    values['nirnaami_lekh_sr_no'] = lists[-1] + 1
                else:
                    values['nirnaami_lekh_sr_no'] = result

        if 'nirnaami_lekh_sr_no' in values:
            values['nirnaami_lekh_display_sr_no'] = "N" + str(values['nirnaami_lekh_sr_no'])

        values['rec_state'] = 'created'

        # ------------- Doc Rec -------------
        related_info = []
        if values['nirnaami_lekh_related_info_lines'] != False and values['nirnaami_lekh_related_info_lines'] != None:

            for rec in values['nirnaami_lekh_related_info_lines']:
                if 'date_of_publishing' not in rec[2]:
                    date_of_publishing = False
                else:
                    date_of_publishing = rec[2]['date_of_publishing']

                if 'date_of_occurance' not in rec[2]:
                    date_of_occurance = False
                else:
                    date_of_occurance = rec[2]['date_of_occurance']

                if 'vikram_samvant_of_publishing' not in rec[2]:
                    vikram_samvant_of_publishing = False
                else:
                    vikram_samvant_of_publishing = rec[2]['vikram_samvant_of_publishing']

                if 'category' not in rec[2]:
                    category = False
                else:
                    category = rec[2]['category']

                if 'person_id' not in rec[2]:
                    person_id = False
                else:
                    person_id = rec[2]['person_id'][0][2]

                if 'sanstha_id' not in rec[2]:
                    sanstha_id = False
                else:
                    sanstha_id = rec[2]['sanstha_id'][0][2]

                if 'mahatma_id' not in rec[2]:
                    mahatma_id = False
                else:
                    mahatma_id = rec[2]['mahatma_id'][0][2]

                if 'samiti_id' not in rec[2]:
                    samiti_id = False
                else:
                    samiti_id = rec[2]['samiti_id'][0][2]

                a = [date_of_publishing, date_of_occurance, vikram_samvant_of_publishing, category,
                     rec[2]['reference_type'],
                     person_id, sanstha_id, mahatma_id, samiti_id]
                related_info.append(a)

        tag_ids = False
        if values['tags_id'] != False and values['tags_id'] != None:
            tag_ids = values['tags_id'][0][2]

        tahrav_ids = False
        if values['tharav'] != False and values['tharav'] != None:
            tahrav_ids = values['tharav'][0][2]

        nirnaami_sr_no = values['nirnaami_lekh_sr_no']

        nirnaami_lekh_display_sr_no = values['nirnaami_lekh_display_sr_no']

        subject = values['subject']

        description = values['description']

        remark = values['remark']

        star_rating = values['star_rating']

        vals = {
            'doc_type': 'nirnaami_lekh',
            'sr_no': nirnaami_sr_no,
            'sr_no_prefix': nirnaami_lekh_display_sr_no,
            'subject': subject,
            'tags_id': tag_ids,
            'tharav_id': tahrav_ids,
            'description': description,
            'related_info': related_info,
            'remark': remark,
            'star_rating': star_rating,
            'nirnaami_lekh_ids': self.id,
        }

        doc_id = self.env['documents.model'].create(vals)

        values['doc_ref'] = doc_id

        record = super(NirnaamiLekh, self).create(values)

        return record

    def write(self, vals):
        doc_vals = {}
        if 'subject' in vals:
            doc_vals['subject'] = vals['subject']

        if 'tags_id' in vals:
            doc_vals['tags_id'] = vals['tags_id']

        if 'tharav' in vals:
            doc_vals['tharav_id'] = vals['tharav']

        if 'description' in vals:
            doc_vals['description'] = vals['description']

        if 'remark' in vals:
            doc_vals['remark'] = vals['remark']

        if 'star_rating' in vals:
            doc_vals['star_rating'] = vals['star_rating']

        if len(doc_vals) > 0:
            RelatedDocObj = self.env['documents.model'].search([('id', '=', self[-1].doc_ref)])
            if RelatedDocObj not in [False, None] and len(RelatedDocObj) > 0:
                RelatedDocObj.write(doc_vals)

        res = super(NirnaamiLekh, self).write(vals)
        return res

    def unlink(self):
        for rec in self:
            DocumentObj = rec.env['documents.model'].search([('id', '=', rec.doc_ref)])
            if DocumentObj:
                for rec in DocumentObj:
                    rec.can_delete = True
                    rec.unlink()

        return super(NirnaamiLekh, self).unlink()

    @api.onchange('nirnaami_lekh_related_info_lines')
    def _get_nirnaami_lekh_related_info_lines_copy(self):

        if self.nirnaami_lekh_related_info_lines != False and self.nirnaami_lekh_related_info_lines != None:
            news_heading = ""
            person_str = ""
            sanstha_str = ""
            mahatma_str = ""
            paksh_str = ""
            date_of_occurance = ""
            person = []
            sanstha = []
            mahatma = []
            paksh = []

            n = 1
            a = 1
            b = 1
            c = 1
            d = 1

            for rec in self.nirnaami_lekh_related_info_lines:

                if rec.news_heading != False and rec.news_heading != None:
                    news_heading += "#" + str(n) + ". " + str(rec.news_heading) + ",  "

                for data in rec.person_id:
                    if data.id != False and data.id != None:
                        if data.person_name not in person:
                            person.append(data.person_name)

                for data in rec.sanstha_id:
                    if data.id != False and data.id != None:
                        if data.sanstha_name not in sanstha:
                            sanstha.append(data.sanstha_name)

                for data in rec.mahatma_id:
                    if data.id != False and data.id != None:
                        if data.complete_mahatma_name not in mahatma:
                            mahatma.append(data.complete_mahatma_name)

                for data in rec.paksh_id:
                    if data.id != False and data.id != None:
                        if data.paksh_name not in paksh:
                            paksh.append(data.paksh_name)

                n += 1

            if len(person) >= 0:
                for data in person:
                    person_str += "#" + str(a) + "." + data + ", "
                    a += 1
            else:
                person_str = ""

            if len(sanstha) >= 0:
                for data in sanstha:
                    sanstha_str += "#" + str(b) + "." + data + ", "
                    b += 1
            else:
                sanstha_str = ""

            if len(mahatma) >= 0:
                for data in mahatma:
                    mahatma_str += "#" + str(c) + "." + data + ", "
                    c += 1
            else:
                mahatma_str = ""

            if len(paksh) >= 0:
                for data in paksh:
                    paksh_str += "#" + str(d) + "." + data + ", "
                    d += 1
            else:
                paksh_str = ""

            self.nirnaami_lekh_news_heading_copy = news_heading
            self.nirnaami_lekh_person_copy = person_str
            self.nirnaami_lekh_sanstha_copy = sanstha_str
            self.nirnaami_lekh_mahatma_copy = mahatma_str
            self.paksh_copy = paksh_str

    @api.constrains('nirnaami_lekh_sr_no')
    def _check_nirnaami__lekh_sr_no(self):
        if self.nirnaami_lekh_sr_no != False and self.nirnaami_lekh_sr_no != None:
            if len(str(self.nirnaami_lekh_sr_no)) > 11:
                raise ValidationError("Nirnaami Lekh Sr.No. should must be of 11 character Max.")
        lists = []
        NirnaamiLekhObj = self.env['nirnaami.lekh.model'].search([('id', '!=', self.id)])
        if NirnaamiLekhObj:
            for rec in NirnaamiLekhObj:
                lists.append(rec.nirnaami_lekh_sr_no)

        lists.sort()
        last_element = 0
        zero_count = 0
        result = None
        for data in lists:
            if data == 0 and zero_count < 1:
                zero_count += 1
                continue
            elif (data - 1) != last_element:
                result = last_element + 1
                break
            last_element = data

        if self.nirnaami_lekh_sr_no > 0:
            if self.nirnaami_lekh_sr_no in lists:
                if result == None:
                    raise ValidationError("Sr.No. " + str(
                        self.nirnaami_lekh_sr_no) + " is already taken, You can use any value greater than " + str(
                        lists[-1]) + ".")

                else:
                    raise ValidationError(
                        "Sr.No. " + str(self.nirnaami_lekh_sr_no) + " is already taken, You can use '" + str(
                            result) + "' or any value greater than " + str(lists[-1]) + ".")

        else:
            if len(lists) >= 1:
                if result == None:
                    self.nirnaami_lekh_sr_no = lists[-1] + 1
                else:
                    self.nirnaami_lekh_sr_no = result

    #   ================ VALIDATIONS

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

    @api.constrains('total_page')
    def _check_total_page(self):
        if self.total_page != False and self.total_page != None:
            if len(self.total_page) > 11:
                raise ValidationError("Total Page should must be of 11 character Max.")

    @api.constrains('copy')
    def _check_copy(self):
        if self.copy != False and self.copy != None:
            if len(str(self.copy)) > 11:
                raise ValidationError("Copy should must be of 11 character Max.")

    @api.constrains('remark')
    def _check_remark(self):
        if self.remark != False and self.remark != None:
            if len(self.remark) > 1000:
                raise ValidationError("remark should must be of 1000 character Max.")


class NirnaamiLekhRelatedInfo(models.Model):
    _name = 'nirnaami.lekh.related.info.model'
    _description = 'Nirnaami Lekh Related Info'
    _rec_name = 'news_heading'

    @api.onchange('reference_type')
    def _get_reference_domain(self):
        if self.reference_type != False and self.reference_type != None:
            res = {}
            res['domain'] = {'reference': [('type_of_reference', '=', self.reference_type)]}
            return res
        else:
            pass

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

    nirnaami_lekh_related_info_id = fields.Integer("ID")
    reference_type = fields.Many2one('documents.reference.type', string="Reference Type")
    news_heading = fields.Text("News Heading")
    # news_heading_char = fields.Char("News Heading", size=300)# modified by RPJ

    # widget = "text"
    vikram_samvant_of_publishing = fields.Char("Vikram Samvant Of Publishing")
    samvat_of_occurance = fields.Char("Samvat Of Occurance")
    category = fields.Selection([('original', 'Original Documents'), ('photo_copy', 'Photo Copy OR Xerox'),
                                 ('partial', 'Partial Documents (With no reference)')], "Category", required=True)
    occasion_location = fields.Char("Occasion Location")
    person_id = fields.Many2many('person.model', string="Person")
    sanstha_id = fields.Many2many('sanstha.model', string="Sanstha")
    date_of_publishing = fields.Date("Date Of Publishing")
    date_of_occurance = fields.Date("Date Of Occurance")
    # sahdu_bhagvat_id = fields.Many2many('mahatma.samuday', string="Sadhu Bhagwant")
    mahatma_id = fields.Many2many('mahatma.model', string="Mahatma")
    other_reference_type = fields.Char("Other Reference Type")
    samiti_id = fields.Many2many('samiti.model', string="Samiti")
    paksh_id = fields.Many2many('paksh.model', string="Paksh")
    samuday_id = fields.Many2many('samuday.model', string="Samuday", compute=_get_samuday)

    @api.constrains('news_heading')
    def _check_news_heading(self):
        for rec in self:
            if rec.news_heading != False and rec.news_heading != None:
                if len(rec.news_heading) > 300:
                    raise ValidationError("News Heading should must be of 300 character Max.")

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

    @api.constrains('occasion_location')
    def _check_occasion_location(self):
        for rec in self:
            if rec.occasion_location != False and rec.occasion_location != None:
                if len(rec.occasion_location) > 75:
                    raise ValidationError("Occasion Location should must be of 75 character Max.")