from odoo import models, fields, api
from datetime import datetime, date
from odoo.exceptions import ValidationError


class MagazineType(models.Model):
    _name = 'magazine.type'
    _description = 'Magazine Type'
    _inherit = 'mail.thread'
    _rec_name = 'magazine_name_gujarati'

    magazine_name = fields.Char("English Name", required=True, track_visibility='always')
    magazine_name_hindi = fields.Char("Hindi Name", required=True, track_visibility='always')
    magazine_name_gujarati = fields.Char("Gujarati Name", required=True, track_visibility='always')
    create_date = fields.Date("Created Date", default=date.today())
    state = fields.Selection([
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ], string="Actions", default='pending', track_visibility='always')
    ref_field = fields.Integer("")
    today_date = fields.Datetime("Day", default=datetime.today())
    fix_email = fields.Char("", default="sagar.panchal@aspiresoftserv.com")
    email = fields.Char("", default="sempanchal123@gmail.com")

    def write(self, vals):
        res = super(MagazineType, self).write(vals)

        updates = {}
        for key in vals:
            if key == 'magazine_name':
                updates['Magazine English Name'] = vals[key]

            if key == 'magazine_name_hindi':
                updates['Magazine Hindi Name'] = vals[key]

            if key == 'magazine_name_gujarati':
                updates['Magazine Gujarati Name'] = vals[key]

            if key == 'state':
                updates['Magazine State'] = vals[key]

        self.env.context = dict(self.env.context)
        self.env.context['updates'] = updates

        template_id = self.env.ref('project_j.magazine_type_update_template')
        mail_id = template_id.send_mail(self.id, force_send=True)

        return res

    def accept_magazine_type(self):
        self.write({
            'state': 'accepted',
        })

    def reject_magazine_type(self):
        self.write({
            'state': 'rejected',
        })

    @api.constrains('magazine_name')
    def _check_magazine_name(self):
        if self.magazine_name != False and self.magazine_name != None:
            if len(self.magazine_name) > 75:
                raise ValidationError("English Name should must be of 75 character Max.")

    @api.constrains('magazine_name_hindi')
    def _check_magazine_name_hindi(self):
        if self.magazine_name_hindi != False and self.magazine_name_hindi != None:
            if len(self.magazine_name_hindi) > 75:
                raise ValidationError("Hindi Name should must be of 75 character Max.")

    @api.constrains('magazine_name_gujarati')
    def _check_magazine_name_gujarati(self):
        if self.magazine_name_gujarati != False and self.magazine_name_gujarati != None:
            if len(self.magazine_name_gujarati) > 75:
                raise ValidationError("Gujarati Name should must be of 75 character Max.")


class Language(models.Model):
    _name = 'language.model'
    _description = 'Language'
    _rec_name = 'language_name'

    language_name = fields.Char("Name", required=True)
    color = fields.Integer("")

    @api.constrains('language_name')
    def _check_language_name(self):
        if self.language_name != False and self.language_name != None:
            if len(self.language_name) > 75:
                raise ValidationError("Language Name should must be of 75 character Max.")


class Magazine(models.Model):
    _name = "magazine.model"
    _description = 'Magazine'
    _rec_name = "name"

    nums = [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
            ('11', 11)
        , ('12', 12), ('13', 13), ('14', 14), ('15', 15), ('16', 16), ('17', 17), ('18', 18), ('19', 19), ('20', 20),
            ('21', 21), ('22', 22), ('23', 23)
        , ('24', 24), ('25', 25), ('26', 26), ('27', 27), ('28', 28), ('29', 29), ('30', 30), ('31', 31)]

    days = [('sun', 'Sunday'), ('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'),
            ('fri', 'Friday'), ('sat', 'Saturday')]

    @api.model
    def _get_language(self):
        return self.env['language.model'].search([('language_name', '=', 'Gujarati')])

    def _get_current_id(self):
        self.current_id = self.id

    def _get_lekh(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                LekhObj = self.env['lekh.model'].search([('lekh_related_info_lines.reference_type', '=', 'magazine'), (
                    'lekh_related_info_lines.magazine_reference.id', '=', rec.id)])

                if len(LekhObj) > 0:
                    rec.lekh_rec = LekhObj
                else:
                    rec.lekh_rec = False

    def _get_tags(self):
        for rec in self:
            tag_ids = []
            if rec.lekh_rec != False and rec.lekh_rec != None:
                if len(rec.lekh_rec) > 0:
                    for lekh in rec.lekh_rec:
                        if lekh.tags_id != False and lekh.tags_id != None:
                            if len(lekh.tags_id) > 0:
                                for tag in lekh.tags_id:
                                    tag_ids.append(tag.id)

            if len(tag_ids) > 0:
                rec.tags_rec = tag_ids
            else:
                rec.tags_rec = False

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

    # @api.onchange('magazine_social_info_lines', 'magazine_type', 'language_id', 'publication_start_year',
    #               'publication_start_year_vikram_samvant', 'publication_end_year',
    #               'publication_end_year_vikram_samvant')
    def _check_record_complete_status(self):
        for rec in self:
            elements = [None, False]
            if rec.magazine_type not in elements and (rec.language_id not in elements and len(
                    rec.language_id) > 0) and rec.publication_start_year not in elements and rec.publication_start_year_vikram_samvant not in elements and rec.publication_end_year not in elements and rec.publication_end_year_vikram_samvant not in elements and (
                    rec.magazine_social_info_lines not in elements and len(rec.magazine_social_info_lines) > 0):
                for social_info in rec.magazine_social_info_lines:

                    if social_info.contact_person in elements or social_info.phone_no in elements or social_info.address in elements:
                        rec.complete_record = False
                        break

                    else:
                        rec.complete_record = True

                        if rec.magazine_type == 'mashik':
                            if rec.publication_date_nums in elements:
                                rec.complete_record = False

                        elif rec.magazine_type == 'saptahik':
                            if rec.publication_date_days in elements:
                                rec.complete_record = False

                        elif rec.magazine_type in ['trimasik', 'dvimasik', 'ardhamasik', 'varsik']:
                            if rec.publication_date in elements:
                                rec.complete_record = False

            else:
                rec.complete_record = False

    # Update Samuday based on the selected Mahatma
    @api.onchange('mahatma_id')
    def update_samuday(self):
        self.samuday_ids = False
        self.samuday_ids = self.mahatma_id.mapped('samuday_id').ids

    name = fields.Char("Magazine Name", required=True)
    tags_id = fields.Many2many('lekh.tags.model', string="Tags")
    magazine_type = fields.Many2one('magazine.type',string="Magazine Type")
    # language_id = fields.Selection([('english','English'),('gujarati','Gujarati'),('sanskrut','Sanskrut'),('prakrut','Prakrut'),('marathi','Marathi'),('apabharansa','Apabharansa')], 'Language', required=True, default="english")
    language_id = fields.Many2many(
        'language.model', string="Language", default=_get_language, required=True)
    referring_category = fields.Selection(
        [('A', 'A'), ('B', 'B'), ('C', 'C')], "Referring Category")
    severity = fields.Selection(
        [('a', 'A - High'), ('b', 'B - Medium'), ('c', 'C - Low')], "Severity")
    link_magazine = fields.Many2one('magazine.model', "Link Magazine")
    description = fields.Text("Description")

    person_id = fields.Many2many('person.model', string="Person")
    sanstha_id = fields.Many2many('sanstha.model', string="Sanstha")
    mahatma_id = fields.Many2many('mahatma.model', string="Mahatma")  # Renamed from Name Of Mahatma to Mahatma
    remark = fields.Text("Remark")
    # address = fields.Text("Address")

    magazine_social_info_lines = fields.One2many('social.info', 'ref_field', string="Social Info")

    is_discontinued = fields.Boolean("Discontinued")
    not_sure = fields.Boolean("Not Sure")
    # is_magazine_available_in_gg = fields.Boolean(
    #     "Is Magazine Avaiilable in GG")
    is_magazine_available_in_gg = fields.Selection([('બધા અંકો ઉપલબ્ધ નથી', 'બધા અંકો ઉપલબ્ધ નથી'), ('સંસ્થામાં આવતું નહોતું', 'સંસ્થામાં આવતું નહોતું'), ('ખ્યાલ નથી', 'ખ્યાલ નથી'), ('બધા જ અંકો ઉપલબ્ધ છે ','બધા જ અંકો ઉપલબ્ધ છે ')],
                                                   string="Is Magazine Avaiilable in GG")
    monitor_for_abusive_contents = fields.Boolean(
        "Monitor For Abusive Contents")
    magazine_group = fields.Char("Magazine Group")
    reader = fields.Many2many('users.model', 'reader_field', string="Reader")
    receiver = fields.Many2many('users.model', 'reciever_field', string="Receiver")
    paksh_id = fields.Many2many('paksh.model', string="Paksh")
    samuday_ids = fields.Many2many('samuday.model', 'magazine_samuday_model_rel', 'magazine_id', 'samuday_id',
                                   string="Samuday")  # Newly added as per PRJ-11
    person_copy = fields.Char("Person")
    sanstha_copy = fields.Char("Sanstha")
    mahatma_copy = fields.Char("Mahatma")
    language_copy = fields.Char("Language")
    paksh_copy = fields.Char("Paksh")

    magazine_start_date = fields.Date("Magazine Start Date")
    discontinue_date = fields.Date("Discontinue Date")
    ref_id = fields.Integer("Ref. Id.")
    publication_date_nums = fields.Selection(nums, "Publication Date")
    publication_date_days = fields.Selection(days, "Publication Date")
    publication_date = fields.Char("Publication Date")
    current_id = fields.Integer(compute=_get_current_id)
    lekh_rec = fields.One2many('lekh.model', 'lekh_ref_field', string="Lekh", readonly=True, compute=_get_lekh)
    # nirnaami_lekh_rec = fields.One2many('nirnaami.lekh.model', 'nirnaami_lekh_ref_field', 
    # string="Nirnaami Lekh", readonly=True)
    # book_rec = fields.One2many('book.model', 'book_ref_field', string="Book", readonly=True)
    # video_rec = fields.One2many('video.model', 'video_ref_field', string="Video", readonly=True)
    tags_rec = fields.One2many('lekh.tags.model', 'tags_ref_field', string="Tag", readonly=True, compute=_get_tags)
    complete_record = fields.Boolean("Complete Record", compute=_check_record_complete_status, store=True)  # , store=True
    magazine_state = fields.Selection(
        [('Active', 'Active'), ('Discontinued', 'Discontinued'), ('Not Sure', 'Not Sure')], string="Magazine State")
    editor = fields.Char("Editor")
    publication_location = fields.Char("Publication Location")
    publication_start_year = fields.Char("Start of publication year (ઈ.સ)")
    publication_start_year_vikram_samvant = fields.Char("Start of publication year (વિ.સં)")
    publication_end_year = fields.Char("End of publication year (ઈ.સ)")
    publication_end_year_vikram_samvant = fields.Char("End of publication year (વિ.સં)")
    is_magazine_coming_to_gg = fields.Selection(
        [('નિયમિત આવે છે', 'નિયમિત આવે છે'), ('અનિયમિત આવે છે', 'અનિયમિત આવે છે'), ('આવતું નથી', 'આવતું નથી'),
         ('ખ્યાલ નથી', 'ખ્યાલ નથી')], string="Is Magazine Coming to GG?")
    is_emagazine = fields.Boolean("E-Magazine")
    url_for_emagazine = fields.Char("")
    reading_category = fields.Selection(
        [('A', 'A'), ('B', 'B'), ('C', 'C')], string="Reading Category")
    color = fields.Integer("")

    @api.model
    def create(self, values):
        # search = self.env['magazine.model'].search([('name','=',values['name'])])

        # elements = [False, None, '']
        # if values['person_id'] not in elements and len(values['person_id'][0][2])>0:
        #     PersonObj = self.env['person.model'].browse(values['person_id'][0][2])
        #     if PersonObj not in elements and len(PersonObj)>0:
        #         for prsn in PersonObj:
        #             prsn.magazine_id = 

        # if values['sanstha_id'] not in elements and len(values['sanstha_id'][0][2])>0:

        # if values['mahatma_id'] not in elements and len(values['mahatma_id'][0][2])>0:

        record = super(Magazine, self).create(values)
        return record

    def write(self, vals):
        # elements = [None, False]
        # if (self.magazine_type not in elements) and (
        #         self.language_id not in elements and len(self.language_id) > 0) and (
        #         self.publication_start_year not in elements) and (
        #         self.publication_start_year_vikram_samvant not in elements) and (
        #         self.publication_end_year not in elements) and (
        #         self.publication_end_year_vikram_samvant not in elements) and 'magazine_social_info_lines' in vals:#(self.magazine_social_info_lines not in elements and len(self.magazine_social_info_lines) > 0)
        #     for social_info in vals.get('magazine_social_info_lines'):
        #         if social_info[2]:
        #             if type(social_info[1]) != int:
        #                 stop
        #                 if 'virtual' in social_info[1]:
        #                     # if social_info[2].get('contact_person') in elements or social_info.phone_no in elements or social_info.address in elements:
        #                     if social_info[2].get('contact_person') in elements or social_info[2].get('phone_no') in elements or social_info[2].get('address') in elements:
        #                         vals['complete_record'] = False
        #                         break
        #
        #         else:
        #             vals['complete_record'] = True
        #             if self.magazine_type == 'mashik':
        #                 if self.publication_date_nums in elements:
        #                     vals['complete_record'] = False
        #
        #             elif self.magazine_type == 'saptahik':
        #                 if self.publication_date_days in elements:
        #                     vals['complete_record'] = False
        #
        #             elif self.magazine_type in ['trimasik', 'dvimasik', 'ardhamasik', 'varsik']:
        #                 if self.publication_date in elements:
        #                     vals['complete_record'] = False
        #
        # else:
        #     vals['complete_record'] = False

        if 'monitor_for_abusive_contents' in vals:
            if vals['monitor_for_abusive_contents'] == False:
                AnkObj = self.env['magazine.ank'].search([('magazine_id', '=', self.current_id)])
                if len(AnkObj) > 0:
                    for ank in AnkObj:
                        if ank.state != 'completed':
                            raise ValidationError(
                                "Please Complete the ank: " + ank.ank_name + " of this magazine first.")

        res = super(Magazine, self).write(vals)
        return res

    @api.onchange('link_magazine')
    def _get_link_magazine(self):
        if self.link_magazine:
            if self.link_magazine.id != False and self.link_magazine.id != None:
                self.tags_id = self.link_magazine.tags_id
                self.magazine_type = self.link_magazine.magazine_type
                self.language_id = self.link_magazine.language_id
                self.severity = self.link_magazine.severity
                self.referring_category = self.link_magazine.referring_category
                self.description = self.link_magazine.description
                self.person_id = self.link_magazine.person_id
                self.sanstha_id = self.link_magazine.sanstha_id
                self.mahatma_id = self.link_magazine.mahatma_id
                self.is_discontinued = self.link_magazine.is_discontinued
                self.not_sure = self.link_magazine.not_sure
                self.is_magazine_available_in_gg = self.link_magazine.is_magazine_available_in_gg
                self.monitor_for_abusive_contents = self.link_magazine.monitor_for_abusive_contents
                self.magazine_group = self.link_magazine.magazine_group
                self.reader = self.link_magazine.reader
                self.receiver = self.link_magazine.receiver
                self.person_copy = self.link_magazine.person_copy
                self.sanstha_copy = self.link_magazine.sanstha_copy
                self.mahatma_copy = self.link_magazine.mahatma_copy
                self.language_copy = self.link_magazine.language_copy
                self.magazine_start_date = self.link_magazine.magazine_start_date
                self.discontinue_date = self.link_magazine.discontinue_date
                self.publication_date_nums = self.link_magazine.publication_date_nums
                self.publication_date_days = self.link_magazine.publication_date_days
                self.publication_date = self.link_magazine.publication_date
                self.magazine_social_info_lines = self.link_magazine.magazine_social_info_lines

    @api.onchange('paksh_id')
    def _get_magazine_paksh_copy_lines(self):

        if self.paksh_id != False and self.paksh_id != None:

            paksh = ""
            a = 1

            for rec in self.paksh_id:

                if rec.id != False and rec.id != None:
                    paksh += "#" + str(a) + ". " + str(rec.paksh_name) + ",  "
                    a += 1

            self.paksh_copy = paksh

    @api.onchange('person_id')
    def _get_magazine_person_copy_lines(self):

        if self.person_id != False and self.person_id != None:

            person = ""
            a = 1

            for rec in self.person_id:

                if rec.id != False and rec.id != None:
                    person += "#" + str(a) + ". " + str(rec.person_name) + ",  "
                    a += 1

            self.person_copy = person

    @api.onchange('sanstha_id')
    def _get_magazine_sanstha_copy_lines(self):

        if self.sanstha_id != False and self.sanstha_id != None:

            sanstha = ""
            a = 1

            for rec in self.sanstha_id:

                if rec.id != False and rec.id != None:
                    sanstha += "#" + str(a) + ". " + str(rec.sanstha_name) + ",  "
                    a += 1

            self.sanstha_copy = sanstha

    @api.onchange('mahatma_id')
    def _get_magazine_mahatma_copy_lines(self):

        if self.mahatma_id != False and self.mahatma_id != None:

            mahatma = ""
            a = 1

            for rec in self.mahatma_id:

                if rec.id != False and rec.id != None:
                    mahatma += "#" + str(a) + ". " + str(rec.complete_mahatma_name) + ",  "
                    a += 1

            self.mahatma_copy = mahatma

    @api.onchange('language_id')
    def _get_magazine_language_copy(self):

        language = ""
        if self.language_id != False and self.language_id != None:

            for rec in self.language_id:

                if rec.id != False and rec.id != None:
                    language += str(rec.language_name) + ",  "

            self.language_copy = language

    @api.onchange('is_magazine_available_in_gg')
    def _check_is_magazine_available_in_gg(self):
        if self.is_magazine_available_in_gg == 'yes':
            self.monitor_for_abusive_contents = True

    @api.constrains('name')
    def _check_name(self):
        if self.name != False and self.name != None:
            if len(self.name) > 75:
                raise ValidationError("Magazine Name should must be of 75 character Max.")

    @api.constrains('description')
    def _check_description(self):
        if self.description != False and self.description != None:
            if len(self.description) > 10000:
                raise ValidationError("Description should must be of 10000 character Max.")

    @api.constrains('magazine_group')
    def _check_magazine_group(self):
        if self.magazine_group != False and self.magazine_group != None:
            if len(self.magazine_group) > 200:
                raise ValidationError("Magazine Group should must be of 200 character Max.")


class MagazineSearch(models.TransientModel):
    _name = 'magazine.search'
    _description = 'Magazine Search'

    magazine_search_id = fields.Integer("")
    message = fields.Char("", readonly=True)
    magazine_id = fields.One2many('magazine.model', 'ref_id', string="Magazine")
