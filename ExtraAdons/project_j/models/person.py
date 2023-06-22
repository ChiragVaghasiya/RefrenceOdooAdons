from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PersonSamiti(models.Model):
    _name = 'person.samiti'
    _description = 'Person Samiti'
    _inherit = 'mail.thread'
    _rec_name = 'samiti_id'

    samiti_id = fields.Many2one('samiti.model', string="Samiti")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    start_date_vikram_samvant = fields.Char("Start Date Vikram Samvat")
    end_date_vikram_samvant = fields.Char("End Date Vikram Samvat")
    ref_field = fields.Integer("")


class SansthaPosition(models.Model):
    _name = 'sanstha.position'
    _description = 'Sanstha Position'
    _rec_name = 'sanstha_id'

    sanstha_id = fields.Many2one('sanstha.model', string="Sanstha")
    position = fields.Char("Position")
    ref_field = fields.Integer("")


class Person(models.Model):
    _name = 'person.model'
    _description = 'Person'
    _inherit = 'mail.thread'
    _rec_name = 'person_name'

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

    def _get_tharav(self):
        for rec in self:
            rec.tharav_rec = False

            if rec.id != False and rec.id != None:

                paksh_ids = []
                if rec.paksh_id != False and rec.paksh_id != None and len(rec.paksh_id) > 0:

                    for paksh in rec.paksh_id:
                        if paksh.id not in paksh_ids:
                            paksh_ids.append(paksh.id)

                    TharavObj = self.env['tharav.model'].search([('paksh_id.id', 'in', paksh_ids)])

                    if len(TharavObj) > 0:

                        rec.tharav_rec = TharavObj
                    else:
                        rec.tharav_rec = False

    def _check_record_complete_status(self):
        elements = [None, False]
        for rec in self:
            if rec.resident not in elements and rec.phone_no not in elements and rec.address not in elements and (
                    rec.sanstha_post not in elements and len(rec.sanstha_post) > 0):
                for item in rec.sanstha_post:
                    if (item.sanstha_id not in elements and len(item.sanstha_id) > 0) and item.position not in elements:
                        rec.complete_record = True
                    else:
                        rec.complete_record = False
            else:
                rec.complete_record = False

    person_name = fields.Char("Name", required=True, track_visibility='always')
    last_name = fields.Char("Last name", track_visibility='always')
    mahatma_id = fields.Many2one('mahatma.model', "Mahatma", track_visibility='always')
    remark = fields.Text("Remark", track_visibility='always')
    address = fields.Text("Address", track_visibility='always')
    paksh_id = fields.Many2many('paksh.model', string="Paksh", track_visibility='always')
    is_reader = fields.Boolean("Reader", track_visibility='always')
    is_receiver = fields.Boolean("Receiver", track_visibility='always')

    person_social_info_lines = fields.One2many('social.info', 'ref_field', string="Social Info Lines")

    color = fields.Integer("")
    ref_id = fields.Integer("")
    paksh_copy = fields.Char("Paksh")
    samiti_id = fields.One2many('person.samiti', 'ref_field', string="Samiti", track_visibility='always')
    tharav_rec = fields.One2many('tharav.model', 'ref_id', string="Tharav", readonly=True, compute=_get_tharav,
                                 track_visibility='always')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ], string="Actions", default='pending', track_visibility='always')
    rec_state = fields.Selection([('draft', 'Draft'), ('created', 'Created')], default='draft')
    complete_record = fields.Boolean("Complete Record", compute=_check_record_complete_status, store=True)
    today_date = fields.Datetime("Day", default=datetime.today())
    fix_email = fields.Char("", default="sagar.panchal@aspiresoftserv.com")
    email = fields.Char("", default="sempanchal123@gmail.com")

    sr_no = fields.Integer("Sr. No.")
    resident = fields.Char("Resident")
    person_status = fields.Selection([('live', 'Live'), ('not_live', 'Not Live'), ('not_sure', 'Not Sure')],
                                     string="Is Live?")

    sanstha_post = fields.One2many('sanstha.position', 'ref_field', string="Associated Sanstha - Post")
    samuday_id = fields.Many2many('samuday.model', string="Samuday")
    associated_magazine = fields.Many2many('magazine.model', string="Associated Magazine Name")

    def write(self, vals):
        res = super(Person, self).write(vals)

        updates = {}
        for key in vals:
            if key == 'person_name':
                updates['Person Name'] = vals[key]

            if key == 'last_name':
                updates['Last Name'] = vals[key]

            if key == 'remark':
                updates['Remark'] = vals[key]

            if key == 'address':
                updates['Address'] = vals[key]

            if key == 'is_reader':
                updates['Reader'] = vals[key]

            if key == 'is_receiver':
                updates['Receiver'] = vals[key]

            if key == 'phone_no':
                updates['Phone No'] = vals[key]

            if key == 'email':
                updates['Email'] = vals[key]

            if key == 'you_tube':
                updates['You Tube'] = vals[key]

            if key == 'whatsapp_no':
                updates['Whatsapp No'] = vals[key]

            if key == 'facebook_field':
                updates['Facebook'] = vals[key]

            if key == 'Website':
                updates['Website'] = vals[key]

            if key == 'state':
                updates['State'] = vals[key]

            if key == 'complete_record':
                updates['Is Record Completed?'] = vals[key]

        self.env.context = dict(self.env.context)
        self.env.context['updates'] = updates

        template_id = self.env.ref('project_j.person_update_mail_template')
        mail_id = template_id.send_mail(self.id, force_send=True)

        return res

    def accept_person(self):
        self.write({
            'state': 'accepted',
        })

    def reject_person(self):
        self.write({
            'state': 'rejected',
        })

    @api.onchange('samiti_id')
    def _update_samiti(self):
        if len(self.samiti_id) > 0:
            for samiti in self.samiti_id:
                SamitiObj = self.env['samiti.model'].search([('id', '=', samiti.samiti_id.id)])
                if len(SamitiObj) > 0:
                    SamitiObj.samiti_person_id = [(0, 0, {'person_id': self._origin.id, 'start_date': samiti.start_date,
                                                          'end_date': samiti.end_date,
                                                          'start_date_vikram_samvant': samiti.start_date_vikram_samvant,
                                                          'end_date_vikram_samvant': samiti.end_date_vikram_samvant})]

    @api.onchange('paksh_id')
    def _get_sanstha_paksh_copy_lines(self):

        if self.paksh_id != False and self.paksh_id != None:

            paksh = ""
            a = 1

            for rec in self.paksh_id:

                if rec.id != False and rec.id != None:
                    paksh += "#" + str(a) + ". " + str(rec.paksh_name) + ",  "
                    a += 1

            self.paksh_copy = paksh

    @api.model
    def create(self, values):
        values['rec_state'] = 'created'
        record = super(Person, self).create(values)

        return record

    @api.constrains('person_name')
    def _check_person_name(self):
        if self.person_name != False and self.person_name != None:
            if len(self.person_name) > 250:
                raise ValidationError("Person Name should must be of 250 character Max.")

    @api.constrains('remark')
    def _check_remark(self):
        if self.remark != False and self.remark != None:
            if len(self.remark) > 1000:
                raise ValidationError("Remark should must be of 1000 character Max.")

    @api.constrains('address')
    def _check_address(self):
        if self.address != False and self.address != None:
            if len(self.address) > 2000:
                raise ValidationError("Address should must be of 2000 character Max.")

    def unlink(self):

        for rec in self:

            relations = ""
            LekhObj = self.env['lekh.model'].search([('lekh_related_info_lines.person_id.id', '=', rec.id)])
            if LekhObj:
                relations += "Lekh, "

            NirnaamiLekhObj = self.env['nirnaami.lekh.model'].search(
                [('nirnaami_lekh_related_info_lines.person_id.id', '=', rec.id)])
            if NirnaamiLekhObj:
                relations += "Nirnaami Lekh, "

            VideoObj = self.env['video.model'].search([('person_id.id', '=', rec.id)])
            if VideoObj:
                relations += "Video, "

            BookObj = self.env['book.model'].search([('person_id.id', '=', rec.id)])
            if BookObj:
                relations += "Book, "

            MagazineObj = self.env['magazine.model'].search([('person_id.id', '=', rec.id)])
            if MagazineObj:
                relations += "Magazine, "

            if relations != "":
                raise ValidationError("You can not delete these record it has relation with " + relations + "model.")

            return super(Person, self).unlink()
