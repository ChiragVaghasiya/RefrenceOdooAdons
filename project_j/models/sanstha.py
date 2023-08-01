from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PramukhTrustee(models.Model):
    _name = 'pramukh.trustee'
    _description = 'Pramukh Trustee'
    _rec_name = 'person_id'

    person_id = fields.Many2one('person.model', string="Person")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    ref_field = fields.Integer("")


class Sanstha(models.Model):
    _name = 'sanstha.model'
    _description = 'Sanstha'
    _inherit = 'mail.thread'
    _rec_name = 'sanstha_name'

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
            paksh_list = []
            if rec.id != False and rec.id != None:
                if rec.paksh_id != None and rec.paksh_id != False and len(rec.paksh_id) > 0:
                    for paksh in rec.paksh_id:
                        if paksh.id not in paksh_list:
                            paksh_list.append(paksh.id)

                if len(paksh_list) > 0:

                    TharavObj = self.env['tharav.model'].search([('paksh_id.id', 'in', paksh_list)])
                    if len(TharavObj) > 0:
                        rec.tharav_rec = TharavObj
                    else:
                        rec.tharav_rec = False

    def _check_record_complete_status(self):
        elements = [None, False]
        for rec in self:
            if rec.location not in elements and rec.status not in elements and rec.contact_person not in elements and rec.phone_no not in elements and rec.address not in elements and (
                    rec.tag_id not in elements and len(rec.tag_id) > 0):
                rec.complete_record = True
            else:
                rec.complete_record = False

    sanstha_name = fields.Char("Name", required=True, track_visibility='always')
    mahatma_id = fields.Many2one('mahatma.model', "Mahatma", track_visibility='always')
    tag_id = fields.Many2many('lekh.tags.model', string="Tags", track_visibility='always')
    description = fields.Text("Description", track_visibility='always')
    remark = fields.Text("Remark", track_visibility='always')
    address = fields.Text("Address", track_visibility='always')
    paksh_id = fields.Many2one('paksh.model', string="Paksh", track_visibility='always')
    paksh_copy = fields.Char("Paksh")

    sanstha_social_info_lines = fields.One2many('social.info', 'ref_field', string="Social Info Lines")

    pramukh = fields.Char("Pramukh", track_visibility='always')
    trustee = fields.Char("Trustee", track_visibility='always')
    color = fields.Integer("")
    ref_id = fields.Integer("")
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

    location = fields.Char("Sanstha Located At")
    other_name = fields.Char("Other Name")
    contact_person = fields.Char("Contact Person")
    head_sanstha = fields.Many2one('sanstha.model', string="Head Sanstha")
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive'), ('not_sure', 'Not Sure')], "Status")
    pramukh = fields.One2many('pramukh.trustee', 'ref_field', string="Pramukh")
    trustee = fields.One2many('pramukh.trustee', 'ref_field', string="Trustee")
    associated_person = fields.Many2many('person.model', string="Associated Person")
    twitter_account_name = fields.Char("Twitter Account Name")
    twitter_account_link = fields.Char("Twitter Account Link")
    instagram = fields.Char("Instagram")
    instagram_link = fields.Char("Instagram Link")
    samuday_id = fields.Many2one('samuday.model', string="Samuday")
    associated_magazine = fields.Many2many('magazine.model', string="Associated Magazine Name")

    def write(self, vals):
        res = super(Sanstha, self).write(vals)

        updates = {}
        for key in vals:
            if key == 'sanstha_name':
                updates['Sanstha Name'] = vals[key]

            if key == 'description':
                updates['Description'] = vals[key]

            if key == 'remark':
                updates['Remark'] = vals[key]

            if key == 'address':
                updates['Address'] = vals[key]

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

            if key == 'pramukh':
                updates['Pramukh'] = vals[key]

            if key == 'trustee':
                updates['Trustee'] = vals[key]

            if key == 'state':
                updates['State'] = vals[key]

            if key == 'complete_record':
                updates['Is Record Completed?'] = vals[key]

        self.env.context = dict(self.env.context)
        self.env.context['updates'] = updates

        template_id = self.env.ref('project_j.sanstha_update_mail_template')
        mail_id = template_id.send_mail(self.id, force_send=True)

        return res

    def accept_sanstha(self):
        self.write({
            'state': 'accepted',
        })

    def reject_sanstha(self):
        self.write({
            'state': 'rejected',
        })

    @api.model
    def create(self, values):
        values['rec_state'] = 'created'
        record = super(Sanstha, self).create(values)

        return record

    @api.onchange('paksh_id')
    def _get_sanstha_paksh_copy_lines(self):

        if self.paksh_id != False and self.paksh_id != None:

            paksh = ""
            a = 1

            for rec in self.paksh_id:

                if rec.id != False and rec.id != None:
                    paksh += "#" + str(a) + ". " + str(rec.paksh_name_gujarati) + ",  "
                    a += 1

            self.paksh_copy = paksh

    @api.constrains('sanstha_name')
    def _check_sanstha_name(self):
        if self.sanstha_name != False and self.sanstha_name != None:
            if len(self.sanstha_name) > 250:
                raise ValidationError("Sanstha Name should must be of 250 character Max.")

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

    @api.constrains('description')
    def _check_description(self):
        if self.description != False and self.description != None:
            if len(self.description) > 2000:
                raise ValidationError("Description should must be of 2000 character Max.")

    def unlink(self):

        for rec in self:

            relations = ""
            LekhObj = self.env['lekh.model'].search([('lekh_related_info_lines.sanstha_id.id', '=', rec.id)])
            if LekhObj:
                relations += "Lekh, "

            NirnaamiLekhObj = self.env['nirnaami.lekh.model'].search(
                [('nirnaami_lekh_related_info_lines.sanstha_id.id', '=', rec.id)])
            if NirnaamiLekhObj:
                relations += "Nirnaami Lekh, "

            VideoObj = self.env['video.model'].search([('sanstha_id.id', '=', rec.id)])
            if VideoObj:
                relations += "Video, "

            BookObj = self.env['book.model'].search([('sanstha_id.id', '=', rec.id)])
            if BookObj:
                relations += "Book, "

            MagazineObj = self.env['magazine.model'].search([('sanstha_id.id', '=', rec.id)])
            if MagazineObj:
                relations += "Magazine, "

            if relations != "":
                raise ValidationError("You can not delete these record it has relation with " + relations + "model.")

        return super(Sanstha, self).unlink()
