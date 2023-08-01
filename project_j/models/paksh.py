from odoo import models, fields, api
from datetime import datetime, date
from odoo.exceptions import ValidationError


class Paksh(models.Model):
    _name = 'paksh.model'
    _description = 'Paksh'
    _inherit = 'mail.thread'
    _rec_name = 'paksh_name_gujarati'

    def _get_samuday(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                SamudayObj = self.env['samuday.model'].search([('paksh_id2', '=', rec.id)])
                if len(SamudayObj) > 0:
                    rec.samuday_rec = SamudayObj
                else:
                    rec.samuday_rec = False

    def _get_mahatma(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                MahatmaObj = self.env['mahatma.model'].search([('paksh_id', '=', rec.id)])
                if len(MahatmaObj) > 0:
                    rec.mahatma_rec = MahatmaObj
                else:
                    rec.mahatma_rec = False

    def _get_magazine(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                MagazineObj = self.env['magazine.model'].search([('paksh_id.id', '=', rec.id)])
                if len(MagazineObj) > 0:
                    rec.magazine_rec = MagazineObj
                else:
                    rec.magazine_rec = False

    def _get_tharav(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                TharavObj = self.env['tharav.model'].search([('paksh_id', '=', rec.id)])
                if len(TharavObj) > 0:
                    rec.tharav_rec = TharavObj
                else:
                    rec.tharav_rec = False

    def _get_lekh(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                LekhObj = self.env['lekh.model'].search([('lekh_related_info_lines.samuday_id.paksh_id', '=', rec.id)])
                if len(LekhObj) > 0:
                    rec.lekh_rec = LekhObj
                else:
                    rec.lekh_rec = False

    def _get_sanstha(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                SansthaObj = self.env['sanstha.model'].search([('paksh_id.id', '=', rec.id)])
                if len(SansthaObj) > 0:
                    rec.sanstha_rec = SansthaObj
                else:
                    rec.sanstha_rec = False

    def _get_person(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                PersonObj = self.env['person.model'].search([('paksh_id', '=', rec.id)])
                if len(PersonObj) > 0:
                    rec.person_rec = PersonObj
                else:
                    rec.person_rec = False

    def _get_tags(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                tag_ids = []

                if rec.magazine_rec != False and rec.magazine_rec != None:

                    for magazine in rec.magazine_rec:
                        if magazine.tags_id != False and magazine.tags_id != None:
                            for tag in magazine.tags_id:
                                tag_ids.append(tag.id)

                if rec.tharav_rec != False and rec.tharav_rec != None:

                    for tharav in rec.tharav_rec:
                        if tharav.tags_id != False and tharav.tags_id != None:
                            for tag in tharav.tags_id:
                                tag_ids.append(tag.id)

                if rec.lekh_rec != False and rec.lekh_rec != None:

                    for lekh in rec.lekh_rec:
                        if lekh.tags_id != False and lekh.tags_id != None:
                            for tag in lekh.tags_id:
                                tag_ids.append(tag.id)

                if rec.sanstha_rec != False and rec.sanstha_rec != None:

                    for sanstha in rec.sanstha_rec:
                        if sanstha.tag_id != False and sanstha.tag_id != None:
                            for tag in sanstha.tag_id:
                                tag_ids.append(tag.id)

                if len(tag_ids) > 0:
                    rec.tags_rec = tag_ids
                else:
                    rec.tags_rec = False

    paksh_name = fields.Char("Paksh Name in English", required=True, track_visibility='always')
    paksh_name_hindi = fields.Char("Paksh Name in Hindi", required=True, track_visibility='always')
    paksh_name_gujarati = fields.Char("Paksh Name in Gujarati", required=True, track_visibility='always')
    create_date = fields.Date("Created Date", defaultt=date.today())

    samuday_rec = fields.One2many('samuday.model', 'samuday_ref_field', string="Samuday", readonly=True,
                                  compute=_get_samuday, track_visibility='always')
    mahatma_rec = fields.One2many('mahatma.model', 'ref_id', string="Mahatma", readonly=True, compute=_get_mahatma,
                                  track_visibility='always')
    magazine_rec = fields.One2many('magazine.model', 'ref_id', string="Magazine", readonly=True, compute=_get_magazine,
                                   track_visibility='always')
    tharav_rec = fields.One2many('tharav.model', 'ref_id', string="Tharav", readonly=True, compute=_get_tharav,
                                 track_visibility='always')
    lekh_rec = fields.One2many('lekh.model', 'lekh_ref_field', string="Lekh", readonly=True, compute=_get_lekh,
                               track_visibility='always')
    # nirnaami_lekh_rec = fields.One2many('nirnaami.lekh.model', 'nirnaami_lekh_ref_field', string="Nirnaami Lekh", readonly=True)
    # book_rec = fields.One2many('book.model', 'book_ref_field', string="Book", readonly=True)
    # video_rec = fields.One2many('video.model', 'video_ref_field', string="Video", readonly=True)
    sanstha_rec = fields.One2many('sanstha.model', 'ref_id', string="Sanstha", readonly=True, compute=_get_sanstha,
                                  track_visibility='always')
    person_rec = fields.One2many('person.model', 'ref_id', string="Person", readonly=True, compute=_get_person,
                                 track_visibility='always')
    tags_rec = fields.Many2many('lekh.tags.model', string="Tag", readonly=True, compute=_get_tags,
                                track_visibility='always')
    color = fields.Integer("")
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
        res = super(Paksh, self).write(vals)

        updates = {}
        for key in vals:
            if key == 'paksh_name':
                updates['Paksh English Name'] = vals[key]

            if key == 'paksh_name_hindi':
                updates['Paksh Hindi Name'] = vals[key]

            if key == 'paksh_name_gujarati':
                updates['Paksh Gujarati Name'] = vals[key]

            if key == 'state':
                updates['Paksh State'] = vals[key]

        self.env.context = dict(self.env.context)
        self.env.context['updates'] = updates

        template_id = self.env.ref('project_j.paksh_update_mail_template')
        mail_id = template_id.send_mail(self.id, force_send=True)

        return res

    def accept_paksh(self):
        self.write({
            'state': 'accepted',
        })

    def reject_paksh(self):
        self.write({
            'state': 'rejected',
        })

    @api.constrains('paksh_name')
    def _check_paksh_name(self):
        if self.paksh_name != False and self.paksh_name != None:
            if len(self.paksh_name) > 175:
                raise ValidationError("Paksh Name in English should must be of 175 character Max.")

    @api.constrains('paksh_name_hindi')
    def _check_paksh_name_hindi(self):
        if self.paksh_name_hindi != False and self.paksh_name_hindi != None:
            if len(self.paksh_name_hindi) > 175:
                raise ValidationError("Paksh Name in Hindi should must be of 175 character Max.")

    @api.constrains('paksh_name_gujarati')
    def _check_paksh_name_gujarati(self):
        if self.paksh_name_gujarati != False and self.paksh_name_gujarati != None:
            if len(self.paksh_name_gujarati) > 175:
                raise ValidationError("Paksh Name Gujarati should must be of 175 character Max.")

    def unlink(self):

        for rec in self:
            relations = ""

            MahatmaObj = self.env['mahatma.model'].search([('paksh_id.id', '=', rec.id)])
            if MahatmaObj:
                relations += "Mahatma, "

            SamudayObj = self.env['samuday.model'].search([('paksh_id2.id', '=', rec.id)])
            if SamudayObj:
                relations += "Samuday, "

            TharavObj = self.env['tharav.model'].search([('paksh_id.id', '=', rec.id)])
            if TharavObj:
                relations += "Tharav, "

            PersonObj = self.env['person.model'].search([('paksh_id.id', '=', rec.id)])
            if PersonObj:
                relations += "Person, "

            if relations != "":
                raise ValidationError("You can not delete these record it has relation with " + relations + "model.")

        return super(Paksh, self).unlink()
