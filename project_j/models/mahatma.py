from odoo import models, fields, api
from odoo.exceptions import ValidationError, Warning
from openerp.tools.translate import _
from langdetect import detect


class MahatmaSamiti(models.Model):
    _name = 'mahatma.samiti'
    _description = 'Mahatma Samiti'
    _rec_name = 'samiti_id'

    samiti_id = fields.Many2one('samiti.model', string="Samiti")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    start_date_vikram_samvant = fields.Char("Start Date Vikram Samvat")
    end_date_vikram_samvant = fields.Char("End Date Vikram Samvat")
    ref_field = fields.Integer("")


class MahatmaSamudayHistory(models.Model):
    _name = 'mahatma.samuday.history'
    _description = 'Mahatma Samuday History'
    _rec_name = 'samuday_id'

    samuday_id = fields.Many2one('samuday.model', string="Samuday")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    ref_field = fields.Integer("")


class Mahatma(models.Model):
    _name = 'mahatma.model'
    _description = 'Mahatma'
    _inherit = 'mail.thread'
    _rec_name = 'complete_mahatma_name'


    def check_duplicate_records(self):

        if self.id != None and self.id != False:
            MahatmaSearchObj = self.env['mahatma.model'].search(
                [('id', '!=', self.id), ('mahatma_name', '=', self.mahatma_name),
                 ('mahatma_presence', '=', self.mahatma_presence)])

            list_mahatma = []
            if MahatmaSearchObj:
                for a in MahatmaSearchObj:
                    if a.designation_copy == self.designation_copy:
                        list_mahatma.append(a.id)

            if len(list_mahatma) > 0:
                # msg = str(len(list_mahatma)) + " - Matching records found."
                mahatma_rec = list_mahatma
                flag = True
            else:
                # msg = "No matching record Found."
                mahatma_rec = False
                flag = False

            message_id = self.env['message.wizard'].create(
                {'message': "", 'mahatma_id': mahatma_rec, 'display_flag': flag, 'display_model': 'mahatma'})
            return {
                'name': _('Duplicate Mahatma'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'message.wizard',
                'res_id': message_id.id,
                'target': 'new'
            }

    # @api.depends('mahatma_name', 'sadhu_gender', 'samuday_id', 'designation_id')
    @api.onchange('mahatma_name', 'sadhu_gender', 'samuday_id', 'designation_id')  # , 'gachhadhipati'
    def _get_prefix_name(self):
        lists = [False, None]
        for rec in self:
            result = ""
            if rec.mahatma_name:
                try:
                    lang_result = detect(rec.mahatma_name)
                    if rec.sadhu_gender == 'સાધુ':

                        if rec.designation_id == 'muni':
                            if lang_result == 'gu':
                                result = "પરમ પૂજ્ય મુનિ"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "परम पूज्य मुनि"
                            else:
                                result = "Param Pujya Muni"
                        elif rec.designation_id == 'ganivarya':
                            if lang_result == 'gu':
                                result = "પરમ પૂજ્ય ગણિવર્ય"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "परम पूज्य गनिवार्य"
                            else:
                                result = "Param Pujya Ganivarya"
                        elif rec.designation_id == 'panyas':
                            if lang_result == 'gu':
                                result = "પરમ પૂજ્ય પાન્યાસ"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "परम पूज्य पन्यास"
                            else:
                                result = "Param Pujya Panyas"
                        elif rec.designation_id == 'upadhyay':
                            if lang_result == 'gu':
                                result = "પરમ પૂજ્ય ઉપાધ્યાય"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "परम पूज्य उपाध्याय"
                            else:
                                result = "Param Pujya Upadhyay"
                        elif rec.designation_id == 'acharya':
                            if lang_result == 'gu':
                                result = "પરમ પૂજ્ય ઉપાધ્યાય"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "परम पूज्य उपाध्याय"
                            else:
                                result = "Param Pujya Acharya"

                        if rec.samuday_id.id in lists and rec.designation_id in lists:

                            if lang_result == 'gu':
                                result = "પરમ પૂજ્ય"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "परम पूज्य"
                            else:
                                result = "Param Pujya"

                        if rec.samuday_id.id not in lists and rec.gachhadhipati == True:

                            if lang_result == 'gu':
                                result = "પરમ પૂજ્ય ગચ્છાધિપતિ"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "परम पूज्य गच्छाधिपति"
                            else:
                                result = "Param Pujya Gachhadhipati"

                    if rec.sadhu_gender == 'સાધ્વી':

                        if rec.samuday_id.id not in lists:
                            if rec.samuday_id.panth_id in ['digambar', 'દિગંબર']:

                                if lang_result == 'gu':
                                    result = "પરમ પૂજ્ય આર્યિકા"
                                elif lang_result in ['hi', 'mr', 'sa']:
                                    result = "परम पूज्य आर्यिका"
                                else:
                                    result = "Param Pujya Aaryika"

                        if rec.samuday_id.id in lists and rec.designation_id2 in lists:

                            if lang_result == 'gu':
                                result = "પરમ પૂજ્ય સાધ્વીશ્રી"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "परम पूज्य साध्वी श्री"
                            else:
                                result = "Param Pujya Sadhvi Shree"

                        if rec.samuday_id.id not in lists and rec.gachhadhipati == True:

                            if lang_result == 'gu':
                                result = "પરમ પૂજ્ય ગચ્છનાયિકા"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "परम पूज्य गछनायिका"
                            else:
                                result = "Param Pujya Gachhanayika"

                    rec.prefix_name = result
                except:
                    raise ValidationError(
                        "Enter valid Mahatma Name")

    @api.onchange('mahatma_name', 'sadhu_gender', 'samuday_id', 'designation_id')
    def _get_suffix_name(self):
        lists = [False, None]
        for rec in self:
            result = ""
            if rec.mahatma_name:
                try:
                    lang_result = detect(rec.mahatma_name)
                    if rec.sadhu_gender == 'સાધુ':
                        if rec.samuday_id.id not in lists:
                            if rec.samuday_id.panth_id == 'digambar' or rec.samuday_id.panth_id == 'sthanakvasi' or rec.samuday_id.panth_id == 'terapanth':
                                if rec.mahatma_name:
                                    if rec.mahatma_name.lower().endswith('sagar') or rec.mahatma_name.endswith(
                                            'સાગર') or rec.mahatma_name.endswith('सागर'):
                                        if lang_result == 'gu':
                                            result = "મહારાજ સાહેબ"
                                        elif lang_result in ['hi', 'mr', 'sa']:
                                            result = "महाराज साहेब"
                                        else:
                                            result = "Maharaj Saheb"
                            elif rec.samuday_id.panth_id != 'digambar' and rec.samuday_id.panth_id != 'sthanakvasi' and rec.samuday_id.panth_id != 'terapanth':
                                if rec.designation_id == "gachhadhipati" or rec.designation_id == "acharya":
                                    if lang_result == 'gu':
                                        result = "સુરીજી મહારાજ સાહેબ"
                                    elif lang_result in ['hi', 'mr', 'sa']:
                                        result = "सुरिजि महाराज साहेब"
                                    else:
                                        result = "Suriji Maharaj Saheb"
                                else:
                                    if rec.mahatma_name:
                                        if rec.mahatma_name.lower().endswith('sagar') or rec.mahatma_name.endswith(
                                                'સાગર') or rec.mahatma_name.endswith('सागर'):
                                            pass
                                        else:
                                            if lang_result == 'gu':
                                                result = "વિજયજી મહારાજ સાહેબ"
                                            elif lang_result in ['hi', 'mr', 'sa']:
                                                result = "विजयजी महाराज साहेब"
                                            else:
                                                result = _("Vijayji Maharaj Saheb")
                                                # result = "Vijayji Maharaj Saheb"
                        else:
                            if lang_result == 'gu':
                                result = "મહારાજ સાહેબ"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "महाराज साहेब"
                            else:
                                result = "Maharaj Saheb"
                    if rec.sadhu_gender == 'સાધ્વી':
                        if rec.samuday_id.id not in lists:
                            if rec.samuday_id.panth_id == 'digambar':
                                if lang_result == 'gu':
                                    result = "શ્રી જી"
                                elif lang_result in ['hi', 'mr', 'sa']:
                                    result = "श्री जी"
                                else:
                                    result = "Shree Ji"
                            else:
                                if lang_result == 'gu':
                                    result = "શ્રીજી મહારાજ સાહેબ"
                                elif lang_result in ['hi', 'mr', 'sa']:
                                    result = "श्रीजी महाराज साहेब"
                                else:
                                    result = "Shreeji Maharaj Saheb"
                        elif rec.designation_id == 'pravartini':
                            if lang_result == 'gu':
                                result = "શ્રીજી મહારાજ સાહેબ"
                            elif lang_result in ['hi', 'mr', 'sa']:
                                result = "श्रीजी महाराज साहेब"
                            else:
                                result = "Shreeji Maharaj Saheb"

                    rec.suffix_name = result
                except:
                    raise ValidationError(
                        "Enter valid Mahatma Name")

    @api.onchange('samuday_id')
    def _get_paksh(self):
        for rec in self:
            rec.paksh_id = False
            # if rec.rec_state != 'created':
            if rec.samuday_id:
                rec.paksh_id = rec.samuday_id.paksh_id2

    # @api.onchange('mahatma_name', 'prefix_name', 'suffix_name')
    @api.depends('mahatma_name', 'prefix_name', 'suffix_name')
    # @api.onchange('mahatma_name', 'prefix_name', 'suffix_name')
    def _get_complete_mahatma_name(self):
        lists = [False, None]
        for rec in self:
            if rec.prefix_name not in lists and rec.mahatma_name not in lists and rec.suffix_name not in lists:
                rec.complete_mahatma_name = rec.prefix_name + " " + rec.mahatma_name + " " + rec.suffix_name

    @api.onchange('sadhu_gender', 'designation_id', 'designation_id2')
    def _get_designation_copy(self):
        for rec in self:

            designation = ""
            result = ""
            designation_dictionary = {'મુનિ': 'મુનિ', 'ગણિ': 'ગણિ', 'પંન્યાસ': 'પંન્યાસ',
                                      'ઉપાધ્યાય': 'ઉપાધ્યાય',
                                      'આચાર્ય': 'આચાર્ય', 'gachhadhipati': 'Gachhadhipati',
                                      'gachhanayika': 'Gachhanayika', 'પ્રવર્તિની': 'પ્રવર્તિની'}
            if rec.sadhu_gender == 'સાધુ':
                if rec.designation_id:
                    designation = rec.designation_id
            else:
                if rec.designation_id2:
                    designation = rec.designation_id2

            if designation != "":
                result = designation_dictionary[designation]
            rec.designation_copy = result

    def _get_samuday(self):
        for rec in self:
            samuday_ids = []
            if rec.samuday_id != None and rec.samuday_id != False:
                samuday_ids.append(rec.samuday_id.id)

            if rec.lekh_rec != False and rec.lekh_rec != None:

                for lekh in rec.lekh_rec:
                    if lekh.lekh_related_info_lines != False and lekh.lekh_related_info_lines != None:
                        if len(lekh.lekh_related_info_lines) > 0:
                            for related_info_lines in lekh.lekh_related_info_lines:
                                if related_info_lines.samuday_id != False and related_info_lines.samuday_id != None:
                                    if len(related_info_lines.samuday_id) > 0:
                                        for samuday in related_info_lines.samuday_id:
                                            samuday_ids.append(samuday.id)

            if len(samuday_ids) > 0:
                rec.samuday_rec = samuday_ids

            else:
                rec.samuday_rec = False

    def _get_magazine(self):

        for rec in self:

            if rec.id != False and rec.id != None:
                MagazineObj = self.env['magazine.model'].search([('mahatma_id.id', '=', rec.id)])
                if len(MagazineObj) > 0:
                    rec.magazine_rec = MagazineObj
                else:
                    rec.magazine_rec = False

    def _get_lekh(self):
        for rec in self:
            LekhObj = self.env['lekh.model'].search([('lekh_related_info_lines.mahatma_id.id', '=', rec.id)])

            if len(LekhObj) > 0:
                rec.lekh_rec = LekhObj
            else:
                rec.lekh_rec = False

    def _get_nirnaami_lekh(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                NirnaamiLekhObj = self.env['nirnaami.lekh.model'].search(
                    [('nirnaami_lekh_related_info_lines.mahatma_id.id', '=', rec.id)])

                if len(NirnaamiLekhObj) > 0:
                    rec.nirnaami_lekh_rec = NirnaamiLekhObj
                else:
                    rec.nirnaami_lekh_rec = False

    def _get_book(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                BookObj = self.env['book.model'].search([('mahatma_id.id', '=', rec.id)])
                if len(BookObj) > 0:
                    rec.book_rec = BookObj
                else:
                    rec.book_rec = False

    def _get_video(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                VideoObj = self.env['video.model'].search([('mahatma_id.id', '=', rec.id)])
                if len(VideoObj) > 0:
                    rec.video_rec = VideoObj
                else:
                    rec.video_rec = False

    def _get_tags(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                tag_ids = []

                if rec.lekh_rec != False and rec.lekh_rec != None:

                    for lekh in rec.lekh_rec:
                        if lekh.tags_id != False and lekh.tags_id != None:
                            for tag in lekh.tags_id:
                                tag_ids.append(tag.id)

                if rec.nirnaami_lekh_rec != False and rec.nirnaami_lekh_rec != None:

                    for nirnaami_lekh in rec.nirnaami_lekh_rec:
                        if nirnaami_lekh.tags_id != False and nirnaami_lekh.tags_id != None:
                            for tag in nirnaami_lekh.tags_id:
                                tag_ids.append(tag.id)

                if rec.book_rec != False and rec.book_rec != None:

                    for book in rec.book_rec:
                        if book.tags_id != False and book.tags_id != None:
                            for tag in book.tags_id:
                                tag_ids.append(tag.id)

                if rec.video_rec != False and rec.video_rec != None:

                    for video in rec.video_rec:
                        if video.tags_id != False and video.tags_id != None:
                            for tag in video.tags_id:
                                tag_ids.append(tag.id)

                if len(tag_ids) > 0:
                    rec.tags_rec = tag_ids
                else:
                    rec.tags_rec = False

    def _get_views(self):
        for rec in self:
            view = []
            a = 0

            if rec.samuday_rec != False and rec.samuday_rec != None:
                if len(rec.samuday_rec) > 0:
                    view.append("samuday")

            if rec.magazine_rec != False and rec.magazine_rec != None:
                if len(rec.magazine_rec) > 0:
                    view.append("magazine")

            if rec.tags_rec != False and rec.tags_rec != None:
                if len(rec.tags_rec) > 0:
                    view.append("tags")

            if rec.lekh_rec != False and rec.lekh_rec != None:
                if len(rec.lekh_rec) > 0:
                    a += 1
                    view.append("lekh")

            if rec.nirnaami_lekh_rec != False and rec.nirnaami_lekh_rec != None:
                if len(rec.nirnaami_lekh_rec) > 0:
                    a += 1
                    view.append("nirnaami_lekh")

            if rec.book_rec != False and rec.book_rec != None:
                if len(rec.book_rec) > 0:
                    a += 1
                    view.append("book")

            if rec.video_rec != False and rec.video_rec != None:
                if len(rec.video_rec) > 0:
                    a += 1
                    view.append("video")

            if a == 0:
                view.append("no_doc")

            rec.views_id = view

    def _get_current_id(self):
        self.current_id = self.id

    def _check_record_complete_status(self):
        elements = [False, None]
        for rec in self:
            if rec.samuday_id not in elements and len(rec.samuday_id) > 0:
                if rec.sadhu_gender == 'સાધુ':
                    if rec.designation_id not in elements:
                        rec.complete_record = True
                    else:
                        rec.complete_record = False

                elif rec.sadhu_gender == 'સાધ્વી':
                    if rec.designation_id2 not in elements:
                        rec.complete_record = True
                    else:
                        rec.complete_record = False
            else:
                rec.complete_record = False

    # @api.onchange('transfer')
    # def _check_transfer(self):
    #     if self.transfer == True:
    #         self.samuday_history_id = [(0, 0, {'samuday_id':1})]

    # @api.onchange('samuday_history_id')
    # def _get_samuday_history_domain(self):
    #     samuday_ids = []
    #     if self.samuday_history_id != False and self.samuday_history_id != None and len(self.samuday_history_id)>0:

    #         for samuday_history in self.samuday_history_id:                
    #             if samuday_history.samuday_id != False and samuday_history.samuday_id != None and len(samuday_history.samuday_id)>0:                    
    #                 samuday_ids.append(samuday_history.samuday_id._origin.id)

    #         if len(samuday_ids)>0:
    #             return {'domain':{'samuday_history_id.samuday_id': [('id','not in',samuday_ids)]}}
    #         else:
    #             pass

    def _check_for_duplicate_flag(self):
        for rec in self:
            if rec.id != None and rec.id != False:
                MahatmaSearchObj = self.env['mahatma.model'].search(
                    [('id', '!=', rec.id), ('mahatma_name', '=', rec.mahatma_name),
                     ('mahatma_presence', '=', rec.mahatma_presence)])

                list_mahatma = []
                if MahatmaSearchObj:
                    for a in MahatmaSearchObj:
                        if a.designation_copy == rec.designation_copy:
                            list_mahatma.append(a.id)

                if len(list_mahatma) > 0:
                    rec.duplicate_flag = True
                    rec.duplicate_msg = "System has found - '" + str(len(list_mahatma)) + "' duplicate records."
                else:
                    rec.duplicate_flag = False
                    rec.duplicate_msg = False

    mahatma_name = fields.Char("Name", required=True, track_visibility='always',
                               help="Write here Mahatma's name only prefix and suffix will be added automatically based on the padvi.")
    prefix_name = fields.Char("Prefix Name", compute=_get_prefix_name)
    suffix_name = fields.Char("Suffix Name", compute=_get_suffix_name)
    complete_mahatma_name = fields.Char("Mahatma Name", compute=_get_complete_mahatma_name)
    guru_id = fields.Many2one('mahatma.model', "Guru")
    designation_start_date = fields.Date("Designation start Date", track_visibility='always')
    remark_field = fields.Text("Remark", track_visibility='always')
    sadhu_gender = fields.Selection(
        [('સાધુ', 'સાધુ'), ('સાધ્વી', 'સાધ્વી')], "Gender",default="સાધુ")
    samuday_id = fields.Many2one('samuday.model', "Samuday", track_visibility='always')
    mahatma_presence = fields.Selection(
        [('yes', 'Yes'), ('no', 'No'), ('not_sure', 'Not Sure'), ], "Is Mahatma live?", default="yes")
    designation_id = fields.Selection([('મુનિ', 'મુનિ'), ('ગણિ', 'ગણિ'), ('પંન્યાસ', 'પંન્યાસ'),
                                       ('ઉપાધ્યાય', 'ઉપાધ્યાય'), ('આચાર્ય', 'આચાર્ય')], "Designation",
                                      track_visibility='always')
    designation_id2 = fields.Selection([('પ્રવર્તિની', 'પ્રવર્તિની')], "Designation", track_visibility='always')
    paksh_id = fields.Many2one('paksh.model', "Paksh", track_visibility='always')
    social_media = fields.Boolean("Social Media")
    image = fields.Binary('')
    color = fields.Integer("")
    designation_copy = fields.Char("Designation", compute=_get_designation_copy)
    current_id = fields.Integer(compute=_get_current_id)
    ref_id = fields.Integer("")

    samuday_rec = fields.One2many('samuday.model', 'samuday_ref_field', compute=_get_samuday, string="Samuday",
                                  readonly=True)
    magazine_rec = fields.One2many('magazine.model', 'ref_id', string="Magazine", compute=_get_magazine, readonly=True)
    lekh_rec = fields.One2many('lekh.model', 'lekh_ref_field', string="Lekh", compute=_get_lekh, readonly=True)
    nirnaami_lekh_rec = fields.One2many('nirnaami.lekh.model', 'nirnaami_lekh_ref_field',
                                        string="Nirnaami Lekh", readonly=True, compute=_get_nirnaami_lekh)
    book_rec = fields.One2many('book.model', 'book_ref_field', string="Book", readonly=True, compute=_get_book)
    video_rec = fields.One2many('video.model', 'video_ref_field', string="Video", readonly=True, compute=_get_video)
    tags_rec = fields.Many2many('lekh.tags.model', string="Tag", readonly=True, compute=_get_tags)
    views_id = fields.Char("Views", compute=_get_views)

    complete_record = fields.Boolean("Complete Record", compute=_check_record_complete_status, store=True)
    diksha_divas = fields.Date("Diksha Divas")
    samiti_id = fields.One2many('mahatma.samiti', 'ref_field', string="Samiti")
    rec_state = fields.Selection([('draft', 'Draft'), ('created', 'Created')], default='draft')
    transfer = fields.Boolean("Transfer")
    samuday_history_id = fields.One2many('mahatma.samuday.history', 'ref_field', string="Samudy History")
    duplicate_flag = fields.Boolean("Duplicate", compute=_check_for_duplicate_flag)
    duplicate_msg = fields.Char("Duplicate Message", compute=_check_for_duplicate_flag)
    other_name = fields.Char("Other Name")
    acharya_pad_date = fields.Date("Acharyapad Date")
    kaaldharm_date = fields.Date("Kaaldharm Date")
    associated_person = fields.Many2many('person.model', string="Associated Person")
    associated_magazine = fields.Many2many('magazine.model', string="Associated Magazine")
    associated_sanstha = fields.Many2many('sanstha.model', string="Associated Sanstha")

    gachhadhipati = fields.Boolean("Gachhnayak")
    social_info_lines = fields.One2many('social.info', 'ref_field', string="Social Info Lines")

    gachhnayika = fields.Boolean("Gachhnayika")
    # is_mahatma_gachhadhipati = fields.Selection([('yes','Yes'),('no','No')], compute=_get_is_mahatma_gachhadhipati)

    @api.onchange('gachhadhipati')
    def _check_gachhadhipati(self):
        a = not self.gachhadhipati
        if self.gachhadhipati:
            elements = [False, None]
            if self.samuday_id not in elements and len(self.samuday_id) > 0:
                if self.samuday_id.gachhadhipati_of_samuday not in elements and len(
                        self.samuday_id.gachhadhipati_of_samuday) > 0:
                    if self.samuday_id.gachhadhipati_of_samuday.mahatma_presence == 'yes':
                        raise ValidationError(
                            "There's already one Gachhadhipati live for '" + self.samuday_id.samuday_name + "' samuday.")

    @api.onchange('samiti_id')
    def _update_samiti(self):
        if len(self.samiti_id) > 0:
            for samiti in self.samiti_id:
                SamitiObj = self.env['samiti.model'].search([('id', '=', samiti.samiti_id.id)])
                if len(SamitiObj) > 0:
                    SamitiObj.samiti_mahatma_id = [(0, 0,
                                                    {'mahatma_id': self._origin.id, 'start_date': samiti.start_date,
                                                     'end_date': samiti.end_date,
                                                     'start_date_vikram_samvant': samiti.start_date_vikram_samvant,
                                                     'end_date_vikram_samvant': samiti.end_date_vikram_samvant})]

    @api.onchange('samuday_id', 'mahatma_presence')
    def _validate_samuday(self):
        if self.samuday_id != None and self.samuday_id != False and len(
                self.samuday_id) > 0 and self.mahatma_presence == 'yes' and self.designation_id != '':
            # if self.samuday_id.gachhadhipati_id not in [False, None]:
            if len(self.samuday_id.gachhadhipati_of_samuday) > 0:
                if self.samuday_id.gachhadhipati_of_samuday.mahatma_presence == 'No':
                    msg = "There's no live Gachhadhipati for " + self.samuday_id.samuday_name + ", You can select designation of this Mahatma as Gachadhipati."
                    message = {
                        'title': _('Assign Gachhadhipati:'),
                        'message': msg
                    }
                    return {'warning': message}

            elif len(self.samuday_id.gachhadhipati_of_samuday) == 0:
                msg = "There's no Gachhadhipati available for the " + self.samuday_id.samuday_name + ", You can set designation of this Mahatma as Gachadhipati."
                message = {
                    'title': _('Assign Gachhadhipati:'),
                    'message': msg
                }
                return {'warning': message}

    @api.onchange('social_media')
    def _get_social_media(self):
        if self.social_media == False:
            self.social_info_lines = False

    @api.model
    def create(self, values):
        # self.check_duplicate_records()

        designation = ""
        result = ""
        designation_dictionary = {'muni': 'Muni', 'ganivarya': 'Ganivarya', 'panyas': 'Panyas', 'upadhyay': 'Upadhyay',
                                  'acharya': 'Acharya', 'gachhadhipati': 'Gachhadhipati',
                                  'gachhanayika': 'Gachhanayika', 'pravartini': 'Pravartini'}

        if values['sadhu_gender'] == 'સાધુ':
            if values['designation_id']:
                designation = values['designation_id']
        else:
            if values['designation_id2']:
                designation = values['designation_id2']

        if designation != "":
            result = designation_dictionary[designation]

        MahatmaSearchObj = self.env['mahatma.model'].search([('mahatma_name', '=', values['mahatma_name']),
                                                             ('mahatma_presence', '=', values['mahatma_presence'])])

        list_mahatma = []
        if MahatmaSearchObj:
            for a in MahatmaSearchObj:
                if a.designation_copy == result:
                    list_mahatma.append(a.id)

        lists = ['False', 'None']
        # if values['mahatma_name'] not in lists:

        #     if values['samuday_id'] != False and values['samuday_id'] != None:

        #         SamudayObj = self.env['samuday.model'].browse(
        #             values['samuday_id'])
        #         if SamudayObj:
        #             result = values['mahatma_name'] + " - " + SamudayObj.samuday_name

        #     else:
        #         result = values['mahatma_name']

        #     vals = {'mahatma_samuday_recs': result}
        #     PersonAndSanstha = self.env['mahatma.samuday'].create(vals)

        if values['mahatma_presence'] == 'yes' and values['designation_id'] == 'gachhadhipati':
            if values['samuday_id'] not in lists and values['mahatma_presence'] not in lists and values[
                'designation_id'] not in lists:
                MahatmaSearchObj = self.env['mahatma.model'].search(
                    [('samuday_id.id', '=', values['samuday_id']), ('mahatma_presence', '=', 'yes'),
                     ('designation_id', '=', 'gachhadhipati')])
                if MahatmaSearchObj:
                    raise ValidationError('There already is one Gachhadhipati Live for "' + str(
                        MahatmaSearchObj.samuday_id.samuday_name) + '" Samuday')

        if len(list_mahatma) > 0:
            values['duplicate_flag'] = True
        values['rec_state'] = 'created'
        record = super(Mahatma, self).create(values)

        # if len(list_mahatma) > 0:
        #     raise Warning( str(len(list_mahatma)) + " - Duplicate Records Found, Please check using Duplicate Button...")

        return record

    # @api.model
    def unlink(self):
        for rec in self:
            relations = ""
            LekhObj = self.env['lekh.model'].search([('lekh_related_info_lines.mahatma_id.id', '=', rec.id)])
            if LekhObj:
                relations += "Lekh, "

            NirnaamiLekhObj = self.env['nirnaami.lekh.model'].search(
                [('nirnaami_lekh_related_info_lines.mahatma_id.id', '=', rec.id)])
            if NirnaamiLekhObj:
                relations += "Nirnaami Lekh, "

            VideoObj = self.env['video.model'].search([('mahatma_id.id', '=', rec.id)])
            if VideoObj:
                relations += "Video, "

            BookObj = self.env['book.model'].search([('mahatma_id.id', '=', rec.id)])
            if BookObj:
                relations += "Book, "

            MagazineObj = self.env['magazine.model'].search([('mahatma_id.id', '=', rec.id)])
            if MagazineObj:
                relations += "Magazine, "

            SansthaObj = self.env['sanstha.model'].search([('mahatma_id.id', '=', rec.id)])
            if SansthaObj:
                relations += "Sanstha, "

            PersonObj = self.env['person.model'].search([('mahatma_id.id', '=', rec.id)])
            if PersonObj:
                relations += "Person, "

            if relations != "":
                raise ValidationError(
                    "You can not delete " + rec.mahatma_name + " record it has relation with " + relations + "model.")

        return super(Mahatma, self).unlink()

    def write(self, vals):

        id_of_samuday = None
        presence_of_mahatma = None
        id_of_designation = None
        lists = [False, None]

        if 'samuday_id' in vals or 'mahatma_presence' in vals or 'designation_id' in vals:

            if 'samuday_id' in vals:
                id_of_samuday = vals['samuday_id']
            else:
                if self.samuday_id.id != None and self.samuday_id.id != False:
                    id_of_samuday = self.samuday_id

            if 'mahatma_presence' in vals:
                presence_of_mahatma = vals['mahatma_presence']
            else:
                presence_of_mahatma = self.mahatma_presence

            if 'designation_id' in vals:
                id_of_designation = vals['designation_id']
            else:
                id_of_designation = self.designation_id

            if presence_of_mahatma == 'yes' and id_of_designation == 'gachhadhipati':

                if id_of_samuday != False and id_of_samuday != None:
                    MahatmaSearchObj = self.env['mahatma.model'].search(
                        [('samuday_id.id', '=', id_of_samuday), ('mahatma_presence', '=', 'yes'),
                         ('designation_id', '=', 'gachhadhipati')])
                    if MahatmaSearchObj:
                        raise ValidationError('There already is one Gachhadhipati Live for "' + str(
                            MahatmaSearchObj.samuday_id.samuday_name) + '" Samuday')

        res = super(Mahatma, self).write(vals)
        return res

    @api.constrains('mahatma_name')
    def _check_name(self):
        # self.action_of_button()
        if self.mahatma_name != False and self.mahatma_name != None:
            if len(self.mahatma_name) > 175:
                raise ValidationError("Name should must be of 175 character Max.")

    @api.constrains('remark_field')
    def _check_remark(self):
        if self.remark_field != False and self.remark_field != None:
            if len(self.remark_field) > 1000:
                raise ValidationError("Remark should must be of 1000 character Max.")
