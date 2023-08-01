from odoo import models, fields, api
from odoo.exceptions import ValidationError
from openerp.tools.translate import _


class LekhTags(models.Model):
    _name = 'lekh.tags.model'
    _description = 'Lekh Tags'
    _rec_name = 'lekh_tag_name'

    lekh_tag_name = fields.Char("Name", required=True)
    color = fields.Integer("")
    tags_ref_field = fields.Integer("")

    @api.constrains('lekh_tag_name')
    def _check_lekh_tag_name(self):
        if self.lekh_tag_name != False and self.lekh_tag_name != None:
            if len(self.lekh_tag_name) > 175:
                raise ValidationError("Tag Name should must be of 175 character Max.")


class Lekh(models.Model):
    _name = 'lekh.model'
    _description = 'Lekh'
    _rec_name = 'lekh_name'

    def check_duplicate_records(self):

        if self.id != None and self.id != False:
            LekhSearchObj = self.env['lekh.model'].search([])

            if len(LekhSearchObj) > 0:
                msg = str(len(LekhSearchObj)) + " matching records found."
                lekh_rec = LekhSearchObj
                flag = True
            else:
                msg = "No matching record Found."
                lekh_rec = False
                flag = False

            message_id = self.env['message.wizard'].create(
                {'message': msg, 'lekh_id': lekh_rec, 'display_flag': flag, 'display_model': 'lekh'})
            return {
                'name': _('Duplicate Search Result'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'message.wizard',
                'res_id': message_id.id,
                'target': 'new'
            }

    @api.onchange('lekh_name', 'subject', 'lekh_related_info_lines', 'total_page')
    def _get_self_id(self):

        if self.id != False:
            if self.id.origin != False and self.id.origin != None:
                self.self_id2 = True

    def _get_current_id(self):
        self.current_id = self.id
        DocumentObj = self.env['documents.model'].search([('id', '=', self.doc_ref)])
        if DocumentObj:
            DocumentObj.lekh_ids = (4, self.current_id)
            DocumentObj.doc_global_related_info = self.lekh_global_related_info

    @api.onchange('lekh_related_info_lines')
    def _get_tharav_domain(self):
        paksh_ids = []
        if self.lekh_related_info_lines != False and self.lekh_related_info_lines != None and len(
                self.lekh_related_info_lines) > 0:

            for related_info_line in self.lekh_related_info_lines:

                if related_info_line.paksh_id != False and related_info_line.paksh_id != None and len(
                        related_info_line.paksh_id) > 0:

                    for paksh in related_info_line.paksh_id:
                        paksh_ids.append(paksh._origin.id)

            if len(paksh_ids) > 0:
                return {'domain': {'tharav': [('paksh_id.id', 'in', paksh_ids)]}}
            else:
                pass

    lekh_name = fields.Char("Name")
    lekh_sr_no = fields.Integer("Sr. No.")

    level1 = fields.Many2one('subject.model',string="Subject 1", domain="[('parent_id', '=', False)]")
    level2 = fields.Many2one('subject.model',string="Subject 2", domain="[('parent_id', '=', level1)]")
    level3 = fields.Many2one('subject.model', string="Subject 3", domain="[('parent_id', '=', level2)]")
    level4 = fields.Many2one('subject.model', string="Subject 4", domain="[('parent_id', '=', level3)]")
    level5 = fields.Many2one('subject.model', string="Subject 5", domain="[('parent_id', '=', level4)]")

    # color = fields.Char("Color")
    tags_id = fields.Many2many('lekh.tags.model', string="Tags")
    # status = fields.Selection([('approved','Approved'), ('pending','Pending'), ('rejected','Rejected')], "Status")
    description = fields.Text("Description")

    lekh_related_info_lines = fields.One2many('lekh.related.info.model', 'lekh_related_id', "Related Info",
                                              required=True)

    tharav = fields.Many2many('tharav.model', string="Tharav")
    total_page = fields.Char("Total Page", required=True)
    link_with_field = fields.Many2many('documents.model', string="Link With Field")
    # link_with_field = fields.Char("Link With Field")
    remark = fields.Text("Remark")
    star_rating = fields.Selection([('one', 'One'), ('two', 'Two'), ('three', 'Three'), ('four', 'Four')],
                                   "Star Ratings for Importance Of Utility")
    is_document_available = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('none', 'None')],
                                             "Is Document Available in GG?", default="none")

    news_heading_copy = fields.Char("News Heading")
    person_copy = fields.Char("Person")
    sanstha_copy = fields.Char("Sanstha")
    mahatma_copy = fields.Char("Mahatma")
    paksh_copy = fields.Char("Paksh")
    date_of_occurance_copy = fields.Char("Date Of Occurance")
    self_id2 = fields.Boolean("ID2", default=False)
    # lekh_se_no_list = fields.Char()
    state = fields.Selection([
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ], string="Actions", default='pending')

    lekh_ref_field = fields.Integer("Lekh Ref.")

    doc_ref = fields.Integer("Doc. Id.")
    current_id = fields.Integer(compute=_get_current_id)

    field_name = fields.Many2many('ir.attachment', string="4")
    lekh_global_related_info = fields.One2many('global.related.info', 'lekh_related_id', string="Test Field")
    rec_state = fields.Selection([('new', 'New'), ('created', 'Created')], default='new')

    def accept_lekh(self):
        self.write({
            'state': 'accepted',
        })

    def reject_lekh(self):
        self.write({
            'state': 'rejected',
        })

    @api.constrains('lekh_related_info_lines')
    def _check_lekh_related_info_lines(self):
        if len(self.lekh_related_info_lines) > 0:
            pass
        else:
            raise ValidationError("Please inseret related Info")

    @api.constrains('total_page')
    def _check_total_page(self):
        if self.total_page <= 0:
            raise ValidationError("Please enter 'Total Page' correctly")

    @api.model
    def create(self, values):

        if 'lekh_related_info_lines' not in values:
            raise ValidationError("Please inseret related Info")

        lists = []
        try:
            LekhObj = self.env['lekh.model'].search([('id', '!=', self.id)])
        except:
            LekhObj = self.env['lekh.model'].search()
        if LekhObj:
            for rec in LekhObj:
                lists.append(rec.lekh_sr_no)

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
        if values['lekh_sr_no'] > 0:
            if values['lekh_sr_no'] in lists:
                if result == None:
                    raise ValidationError("Sr.No. " + str(
                        values['book_sr_no']) + " is already taken, You can use any value greater than " + str(
                        lists[-1]) + ".")

                else:
                    raise ValidationError(
                        "Sr.No. " + str(values['book_sr_no']) + " is already taken, You can use '" + str(
                            result) + "' or any value greater than " + str(lists[-1]) + ".")

        else:
            if len(lists) > 0:
                if result == None:
                    values['lekh_sr_no'] = lists[-1] + 1
                else:
                    values['lekh_sr_no'] = result

        if values['lekh_related_info_lines'] != False and values['lekh_related_info_lines'] != None:

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
            dates = []

            n, a, b, c, d = 1, 1, 1, 1, 1
            try:
                for rec in values['lekh_related_info_lines']:

                    a = [rec.date_of_publishing, rec.date_of_occurance]
                    dates.append(a)

                    if rec[2]['news_heading'] != False and rec[2]['news_heading'] != None:
                        news_heading += "#" + str(n) + ". " + str(rec[2]['news_heading']) + ",  "

                    if rec[2]['person_id'] != False and rec[2]['person_id'] != None:

                        for data in rec[2]['person_id']:
                            if data[2] != False and data[2] != None and len(data[2]) > 0:
                                PersonObj = self.env['person.model'].browse(data[2])
                                if PersonObj:
                                    for info in PersonObj:
                                        if info.person_name not in person:
                                            person.append(info.person_name)

                    if rec[2]['sanstha_id'] != False and rec[2]['sanstha_id'] != None:

                        for data in rec[2]['sanstha_id']:
                            if data[2] != False and data[2] != None and len(data[2]) > 0:
                                SansthaObj = self.env['sanstha.model'].browse(data[2])
                                if SansthaObj:
                                    for info in SansthaObj:
                                        if info.sanstha_name not in sanstha:
                                            sanstha.append(info.sanstha_name)

                    if rec[2]['mahatma_id'] != False and rec[2]['mahatma_id'] != None:

                        for data in rec[2]['mahatma_id']:
                            if data[2] != False and data[2] != None and len(data[2]) > 0:
                                MahatmaObj = self.env['mahatma.model'].browse(data[2])
                                if MahatmaObj:
                                    for info in MahatmaObj:
                                        if info.complete_mahatma_name not in mahatma:
                                            mahatma.append(info.complete_mahatma_name)

                    if rec[2]['paksh_id'] != False and rec[2]['paksh_id'] != None:

                        for data in rec[2]['paksh_id']:
                            if data[2] != False and data[2] != None and len(data[2]) > 0:
                                PakshObj = self.env['paksh.model'].browse(data[2])
                                if PakshObj:
                                    for info in PakshObj:
                                        if info.paksh_name not in paksh:
                                            paksh.append(info.paksh_name)

                    if rec[2]['date_of_occurance'] != False and rec[2]['date_of_occurance'] != None:
                        date_of_occurance += "#" + str(n) + ". " + str(rec[2]['date_of_occurance']) + ",  "

                    n += 1
            except:
                pass

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

            values['news_heading_copy'] = news_heading
            values['person_copy'] = person_str
            values['sanstha_copy'] = sanstha_str
            values['mahatma_copy'] = mahatma_str
            values['paksh_copy'] = paksh_str
            values['date_of_occurance_copy'] = date_of_occurance

        # ------------- Doc Rec -------------
        related_info = []
        if values['lekh_related_info_lines'] != False and values['lekh_related_info_lines'] != None:

            for rec in values['lekh_related_info_lines']:

                if 'date_of_publishing' in rec[2]:
                    date_of_publishing = rec[2]['date_of_publishing']
                else:
                    date_of_publishing = False

                if 'date_of_occurance' in rec[2]:
                    date_of_occurance = rec[2]['date_of_occurance']
                else:
                    date_of_occurance = False

                if 'vikram_samvant_of_publishing' in rec[2]:
                    vikram_samvant_of_publishing = rec[2]['vikram_samvant_of_publishing']
                else:
                    vikram_samvant_of_publishing = False

                if 'category' in rec[2]:
                    category = rec[2]['category']
                else:
                    category = False

                if 'person_id' in rec[2]:
                    person_id = rec[2]['person_id'][0][2]
                else:
                    person_id = False

                if 'sanstha_id' in rec[2]:
                    sanstha_id = rec[2]['sanstha_id'][0][2]
                else:
                    sanstha_id = False

                if 'mahatma_id' in rec[2]:
                    mahatma_id = rec[2]['mahatma_id'][0][2]
                else:
                    mahatma_id = False

                if 'samiti_id' in rec[2]:
                    samiti_id = rec[2]['samiti_id'][0][2]
                else:
                    samiti_id = False

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

        sr_no = values['lekh_sr_no']
        subject = values['subject']
        description = values['description']
        remark = values['remark']
        star_rating = values['star_rating']

        vals = {
            'doc_type': 'lekh',
            'sr_no': sr_no,
            'sr_no_prefix': sr_no,
            'subject': subject,
            'tags_id': tag_ids,
            'tharav_id': tahrav_ids,
            'description': description,
            'related_info': related_info,
            'remark': remark,
            'star_rating': star_rating,
            'lekh_ids': self.id,
        }

        doc_id = self.env['documents.model'].create(vals)

        values['doc_ref'] = doc_id
        values['rec_state'] = 'created'

        record = super(Lekh, self).create(values)

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

        res = super(Lekh, self).write(vals)
        return res

    def unlink(self):
        for rec in self:
            DocumentObj = rec.env['documents.model'].search([('id', '=', rec.doc_ref)])
            if DocumentObj:
                for rec in DocumentObj:
                    rec.can_delete = True
                    rec.unlink()

        return super(Lekh, self).unlink()

    @api.onchange('lekh_related_info_lines')
    def _get_lekh_related_info_lines_copy(self):

        if self.lekh_related_info_lines != False and self.lekh_related_info_lines != None:
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

            n, a, b, c, d = 1, 1, 1, 1, 1

            for rec in self.lekh_related_info_lines:

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

                if rec.date_of_occurance != False and rec.date_of_occurance != None:
                    date_of_occurance += "#" + str(n) + ". " + str(rec.date_of_occurance) + ",  "

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

            self.news_heading_copy = news_heading
            self.person_copy = person_str
            self.sanstha_copy = sanstha_str
            self.mahatma_copy = mahatma_str
            self.paksh_copy = paksh_str
            self.date_of_occurance_copy = date_of_occurance

    @api.constrains('lekh_sr_no')
    def _check_lekh_sr_no(self):
        if self.lekh_sr_no != False and self.lekh_sr_no != None:
            if len(str(self.lekh_sr_no)) > 11:
                raise ValidationError("Lekh Sr.No. should must be of 11 character Max.")
        lists = []
        LekhObj = self.env['lekh.model'].search([('id', '!=', self.id)])
        if LekhObj:
            for rec in LekhObj:
                lists.append(rec.lekh_sr_no)

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
        if self.lekh_sr_no > 0:
            if self.lekh_sr_no in lists:
                if result == None:
                    raise ValidationError("Sr.No. " + str(
                        self.lekh_sr_no) + " is already taken, You can use any value greater than " + str(
                        lists[-1]) + ".")

                else:
                    raise ValidationError("Sr.No. " + str(self.lekh_sr_no) + " is already taken, You can use '" + str(
                        result) + "' or any value greater than " + str(lists[-1]) + ".")

        else:
            if len(lists) >= 1:
                if result == None:
                    self.lekh_sr_no = lists[-1] + 1
                else:
                    self.lekh_sr_no = result

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
        lists = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if self.total_page != False and self.total_page != None:
            if len(self.total_page) > 11:
                raise ValidationError("Total Page should must be of 11 character Max.")

            for ch in str(self.total_page):
                if ch not in lists:
                    raise ValidationError(
                        "Please enter only numerical values in Total Page and no symbols or special characters.")
            # if len(self.total_page) > 11:
            #     raise ValidationError("Total Page should must be of 11 character Max.")

    @api.constrains('remark')
    def _check_remark(self):
        if self.remark != False and self.remark != None:
            if len(self.remark) > 1000:
                raise ValidationError("remark should must be of 1000 character Max.")

    @api.onchange('lekh_related_info_lines')
    def _get_info_from_lekh_related_info(self):

        if self.lekh_related_info_lines != False and self.lekh_related_info_lines != None:
            news_heading = ""
            person = ""
            sanstha = ""
            mahatma = ""
            date_of_occurance = ""

            n = 1
            a = 1
            b = 1
            c = 1
            for rec in self.lekh_related_info_lines:

                if rec.news_heading != False and rec.news_heading != None:
                    news_heading += "#" + str(n) + ". " + str(rec.news_heading) + ",  "
