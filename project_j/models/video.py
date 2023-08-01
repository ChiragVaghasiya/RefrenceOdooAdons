from odoo import models, fields, api
from odoo.exceptions import ValidationError
from openerp.tools.translate import _


class Video(models.Model):
    _name = 'video.model'
    _description = 'Video'
    _rec_name = 'subject'

    def check_duplicate_records(self):

        if self.id != None and self.id != False:
            VideoSearchObj = self.env['video.model'].search([])

            if len(VideoSearchObj) > 0:
                msg = str(len(VideoSearchObj)) + " matching records found."
                video_rec = VideoSearchObj
                flag = True
            else:
                msg = "No matching record Found."
                video_rec = False
                flag = False

            message_id = self.env['message.wizard'].create(
                {'message': msg, 'video_id': video_rec, 'display_flag': flag, 'display_model': 'video'})
            return {
                'name': _('Duplicate Search Result'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'message.wizard',
                'res_id': message_id.id,
                'target': 'new'
            }

    @api.onchange('tags_id', 'video_sr_no', 'status', 'remark', 'tags_id', 'video_display_sr_no', 'subject',
                  'date_of_occurance', 'date_of_publishing', 'person_and_sanstha', 'person_and_sanstha')
    def _get_self_id(self):

        if self.id != False and self.id != None:
            if self.id.origin != False and self.id.origin != None:
                self.video_self_id2 = True

    def _get_current_id(self):
        self.current_id = self.id
        DocumentObj = self.env['documents.model'].search([('id', '=', self.doc_ref)])
        if DocumentObj:
            DocumentObj.video_ids = (4, self.current_id)

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

    @api.onchange('paksh_id')
    def _get_tharav_domain(self):
        if self.paksh_id != False and self.paksh_id != None and len(self.paksh_id) > 0:
            paksh_ids = []
            tharav_ids = []
            for paksh in self.paksh_id:
                paksh_ids.append(paksh._origin.id)

            if len(paksh_ids) > 0:
                return {'domain': {'tharav_id': [('paksh_id.id', 'in', paksh_ids)]}}
            else:
                pass

    video_sr_no = fields.Integer("Sr No.")
    video_display_sr_no = fields.Char("Sr. No.", compute='_get_display_sr_no', store=True, readonly=True)
    subject = fields.Char("Subject")
    tags_id = fields.Many2many('lekh.tags.model', string="Tags")
    vikram_samvat_of_publishing = fields.Char("Vikram Samvat Of Publishing")
    vikram_samvat_of_occurance = fields.Char("Vikram Samvat Of Occurance")
    date_of_occurance = fields.Date("Date of Occurance")
    date_of_publishing = fields.Date("Date of Release")
    tharav_id = fields.Many2many('tharav.model', string="Tharav")
    # status = fields.Selection([('approved','Approved'),('pending','Pending'),('rejected','Rejected')], "Status", default="pending")
    description = fields.Text("Description")

    source = fields.Char("Source")
    person_id = fields.Many2many('person.model', string="Person")
    sanstha_id = fields.Many2many('sanstha.model', string="Sanstha")
    mahatma_id = fields.Many2many('mahatma.model', string="Mahatma")
    remark = fields.Text("Remark")

    category = fields.Selection([('high', 'High'), ('low', 'Low'), ('partial', 'Partial Or Insufficient')], "Category",
                                required=True)
    local_place = fields.Char("Local Place")
    city = fields.Char("City")
    language_id = fields.Many2one('language.model', string="Language")
    # link_with_field = fields.Char("Link With Field")
    link_with_field = fields.Many2many('documents.model', string="Link With Field")

    documents = fields.Binary("Document", required=True)
    star_rating = fields.Selection([('one', 'One'), ('two', 'Two'), ('three', 'Three'), ('four', 'Four')],
                                   "Star Ratings for Importance Of Utility")
    is_document_available = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('none', 'None')],
                                             "Is Document Available in GG?", default="none")

    video_self_id2 = fields.Boolean("ID2", default=False)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ], string="Actions", default='pending')

    video_ref_field = fields.Integer("Video Ref.")
    person_copy = fields.Char("Person")
    sanstha_copy = fields.Char("Sanstha")
    mahatma_copy = fields.Char("Mahatma")
    viddeo_ref_field = fields.Integer("Ref. Id.")
    rec_state = fields.Selection([('draft', 'Draft'), ('created', 'Created')], default='draft')
    doc_ref = fields.Integer("Doc. Id.")
    current_id = fields.Integer(compute=_get_current_id)
    samiti_id = fields.Many2many('samiti.model', string="Samiti")
    paksh_id = fields.Many2many('paksh.model', string="Paksh")
    paksh_copy = fields.Char("Paksh")
    samuday_id = fields.Many2many('samuday.model', string="Samuday", compute=_get_samuday)
    video_global_related_info = fields.One2many('global.related.info', 'ref_field', string="Video Related Info.")

    # def get_stock_file(self):
    #     url = "web/content/?model=" + self._name +"&id=" + str(
    #                 self.id) + "&field=documents&download=true&filename=attachment_download"
    #     return {
    #         'name': 'Downloads',
    #         'type': 'ir.actions.act_url',
    #         'url': url,
    #         'target': 'self',
    #     }

    def get_stock_file(self):
        url = "web/content/?model=" + self._name + "&id=" + str(
            self.id) + "&field=documents&download=true&filename=attachment_download"
        return {
            'name': 'Downloads',
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

        file_dict = {}
        for attachment_id in attachment_ids:
            file_store = attachment_id.store_fname
            if file_store:
                file_name = attachment_id.name
                file_path = attachment_id._full_path(file_store)

        url = '/web/binary/download_document?file_dictionary=%s' % file_dict
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    # def get_stock_file(self):
    #     images_dict = []
    #     for rec in self:
    #         images_dict.append(self.download_image(rec.id))

    #     return images_dict

    # def download_image(self, rec_id):
    #     url = "web/content/?model=" + "video.model" +"&id=" + str(rec_id) + "&field=documents&download=true&filename=attachment_download"
    #     return {
    #         'name': 'Downloads',
    #         'type': 'ir.actions.act_url',
    #         'url': url,
    #         'target': 'self',
    #     }

    @api.onchange('paksh_id')
    def _get_video_paksh_copy_lines(self):

        if self.paksh_id != False and self.paksh_id != None:

            paksh = ""
            a = 1

            for rec in self.paksh_id:

                if rec.id != False and rec.id != None:
                    paksh += "#" + str(a) + ". " + str(rec.paksh_name) + ",  "
                    a += 1

            self.paksh_copy = paksh

    def accept_video(self):
        self.write({
            'state': 'accepted',
        })

    def reject_video(self):
        self.write({
            'state': 'rejected',
        })

    @api.model
    def create(self, values):

        lists = []
        try:
            VideoObj = self.env['video.model'].search([('id', '!=', self.id)])
        except:
            VideoObj = self.env['video.model'].search([])
        if VideoObj:
            for rec in VideoObj:
                lists.append(rec.video_sr_no)

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

        if values['video_sr_no'] > 0:
            if values['video_sr_no'] in lists:
                if result == None:
                    raise ValidationError("Sr.No. " + str(
                        values['video_sr_no']) + " is already taken, You can use any value greater than " + str(
                        lists[-1]) + ".")

                else:
                    raise ValidationError(
                        "Sr.No. " + str(values['video_sr_no']) + " is already taken, You can use '" + str(
                            result) + "' or any value greater than " + str(lists[-1]) + ".")

        else:
            if len(lists) > 0:
                if result == None:
                    values['video_sr_no'] = lists[-1] + 1
                else:
                    values['video_sr_no'] = result

        if 'video_sr_no' in values:
            values['video_display_sr_no'] = "V" + str(values['video_sr_no'])

        values['rec_state'] = 'created'

        # ------------- Doc Rec ------------- 
        related_info = []

        if 'date_of_publishing' in values:
            date_of_publishing = values['date_of_publishing']
        else:
            date_of_publishing = False

        if 'date_of_occurance' in values:
            date_of_occurance = values['date_of_occurance']
        else:
            date_of_occurance = False

        if 'vikram_samvant_of_publishing' in values:
            vikram_samvant_of_publishing = values['vikram_samvant_of_publishing']
        else:
            vikram_samvant_of_publishing = False

        if 'category' in values:
            category = values['category']
        else:
            category = False

        if 'person_id' in values:
            person_id = values['person_id'][0][2]
        else:
            person_id = False

        if 'sanstha_id' in values:
            sanstha_id = values['sanstha_id'][0][2]
        else:
            sanstha_id = False

        if 'mahatma_id' in values:
            mahatma_id = values['mahatma_id'][0][2]
        else:
            mahatma_id = False

        if 'samiti_id' in values:
            samiti_id = values['samiti_id'][0][2]
        else:
            samiti_id = False

        a = [date_of_publishing, date_of_occurance, vikram_samvant_of_publishing, category, False,
             person_id, sanstha_id, mahatma_id, samiti_id]
        related_info.append(a)

        # a = [values['date_of_publishing'], values['date_of_occurance'], values['vikram_samvat_of_publishing'], values['category']]
        # related_info.append(a)

        tag_ids = False
        if values['tags_id'] != False and values['tags_id'] != None:
            tag_ids = values['tags_id'][0][2]

        tahrav_ids = False
        if values['tharav_id'] != False and values['tharav_id'] != None:
            tahrav_ids = values['tharav_id'][0][2]

        video_sr_no = values['video_sr_no']

        video_display_sr_no = values['video_display_sr_no']

        subject = values['subject']

        description = values['description']

        remark = values['remark']

        star_rating = values['star_rating']

        vals = {
            'doc_type': 'video',
            'sr_no': video_sr_no,
            'sr_no_prefix': video_display_sr_no,
            'subject': subject,
            'tags_id': tag_ids,
            'tharav_id': tahrav_ids,
            'description': description,
            'related_info': related_info,
            'remark': remark,
            'star_rating': star_rating,
            'video_ids': self.id,
        }

        doc_id = self.env['documents.model'].create(vals)

        values['doc_ref'] = doc_id
        record = super(Video, self).create(values)

        return record

    def write(self, vals):
        doc_vals = {}
        if 'subject' in vals:
            doc_vals['subject'] = vals['subject']

        if 'tags_id' in vals:
            doc_vals['tags_id'] = vals['tags_id']

        if 'tharav_id' in vals:
            doc_vals['tharav_id'] = vals['tharav_id']

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

        res = super(Video, self).write(vals)
        return res

    def unlink(self):
        for rec in self:
            DocumentObj = rec.env['documents.model'].search([('id', '=', rec.doc_ref)])
            if DocumentObj:
                for rec in DocumentObj:
                    rec.can_delete = True
                    rec.unlink()

        return super(Video, self).unlink()

    @api.onchange('person_id')
    def _get_video_person_copy_lines(self):

        if self.person_id != False and self.person_id != None:

            person = ""
            a = 1

            for rec in self.person_id:

                if rec.id != False and rec.id != None:
                    person += "#" + str(a) + ". " + str(rec.person_name) + ",  "
                    a += 1

            self.person_copy = person

    @api.onchange('sanstha_id')
    def _get_video_sanstha_copy_lines(self):

        if self.sanstha_id != False and self.sanstha_id != None:

            sanstha = ""
            a = 1

            for rec in self.sanstha_id:

                if rec.id != False and rec.id != None:
                    sanstha += "#" + str(a) + ". " + str(rec.sanstha_name) + ",  "
                    a += 1

            self.sanstha_copy = sanstha

    @api.onchange('mahatma_id')
    def _get_video_mahatma_copy_lines(self):

        if self.mahatma_id != False and self.mahatma_id != None:

            mahatma = ""
            a = 1

            for rec in self.mahatma_id:

                if rec.id != False and rec.id != None:
                    mahatma += "#" + str(a) + ". " + str(rec.complete_mahatma_name) + ",  "
                    a += 1

            self.mahatma_copy = mahatma

    @api.constrains('video_sr_no')
    def _check_video_sr_no(self):
        if self.video_sr_no != False and self.video_sr_no != None:
            if len(str(self.video_sr_no)) > 11:
                raise ValidationError("Video Sr.No. should must be of 11 character Max.")
        lists = []
        VideoObj = self.env['video.model'].search([('id', '!=', self.id)])
        if VideoObj:
            for rec in VideoObj:
                lists.append(rec.video_sr_no)

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
        if self.video_sr_no > 0:
            if self.video_sr_no in lists:
                if result == None:
                    raise ValidationError("Sr.No. " + str(
                        self.video_sr_no) + " is already taken, You can use any value greater than " + str(
                        lists[-1]) + ".")

                else:
                    raise ValidationError("Sr.No. " + str(self.video_sr_no) + " is already taken, You can use '" + str(
                        result) + "' or any value greater than " + str(lists[-1]) + ".")

        else:
            if len(lists) >= 1:
                if result == None:
                    self.video_sr_no = lists[-1] + 1
                else:
                    self.video_sr_no = result

    @api.onchange('video_sr_no')
    def _get_display_sr_no(self):
        for rec in self:
            if rec.video_sr_no != False and rec.video_sr_no != None:
                rec.video_display_sr_no = "V" + str(rec.video_sr_no)

    @api.constrains('subject')
    def _check_subject(self):
        if self.subject != False and self.subject != None:
            if len(self.subject) > 3000:
                raise ValidationError("Subject should must be of 3000 character Max.")

    @api.constrains('vikram_samvat_of_publishing')
    def _check_vikram_samvat_of_publishing(self):
        if self.vikram_samvat_of_publishing != False and self.vikram_samvat_of_publishing != None:
            if len(self.vikram_samvat_of_publishing) > 75:
                raise ValidationError("Vikram Samvat Of Publishing should must be of 75 character Max.")

    @api.constrains('vikram_samvat_of_occurance')
    def _check_vikram_samvat_of_occurance(self):
        if self.vikram_samvat_of_occurance != False and self.vikram_samvat_of_occurance != None:
            if len(self.vikram_samvat_of_occurance) > 75:
                raise ValidationError("Vikram Samvat Of Occurance should must be of 75 character Max.")

    @api.constrains('description')
    def _check_description(self):
        if self.description != False and self.description != None:
            if len(self.description) > 10000:
                raise ValidationError("Description should must be of 10000 character Max.")

    @api.constrains('source')
    def _check_source(self):
        if self.source != False and self.source != None:
            if len(self.source) > 250:
                raise ValidationError("Source should must be of 75 character Max.")

    @api.constrains('remark')
    def _check_remark(self):
        if self.remark != False and self.remark != None:
            if len(self.remark) > 1000:
                raise ValidationError("Remark should must be of 1000 character Max.")

    @api.constrains('local_place')
    def _check_local_place(self):
        if self.local_place != False and self.local_place != None:
            if len(self.local_place) > 150:
                raise ValidationError("Local Place should must be of 75 character Max.")

    @api.constrains('city')
    def _check_city(self):
        if self.city != False and self.city != None:
            if len(self.city) > 175:
                raise ValidationError("City should must be of 75 character Max.")
