from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SamitiPerson(models.Model):
    _name = 'samiti.person'
    _description = 'Samiti Person'
    _rec_name = 'person_id'

    person_id = fields.Many2one('person.model', string="Person")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    start_date_vikram_samvant = fields.Char("Start Date Vikram Samvat")
    end_date_vikram_samvant = fields.Char("End Date Vikram Samvat")
    ref_field = fields.Integer("")


class SamitiMahatma(models.Model):
    _name = 'samiti.mahatma'
    _description = 'Samiti Mahatma'
    _rec_name = 'mahatma_id'

    mahatma_id = fields.Many2one('mahatma.model', string="Mahatma")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    start_date_vikram_samvant = fields.Char("Start Date Vikram Samvat")
    end_date_vikram_samvant = fields.Char("End Date Vikram Samvat")
    ref_field = fields.Integer("")


class Samiti(models.Model):
    _name = 'samiti.model'
    _description = 'Samiti'
    _rec_name = 'name'

    def _get_total_members(self):
        for rec in self:
            total = 0
            if len(rec.samiti_person_id) > 0:
                for i in rec.samiti_person_id:
                    total += 1

            if len(rec.samiti_mahatma_id) > 0:
                for i in rec.samiti_mahatma_id:
                    total += 1

            rec.total_members = total

    def _get_lekh(self):
        for rec in self:
            LekhObj = self.env['lekh.model'].search([('lekh_related_info_lines.samiti_id.id', '=', rec.id)])

            if len(LekhObj) > 0:
                rec.lekh_rec = LekhObj
            else:
                rec.lekh_rec = False

    def _get_nirnaami_lekh(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                NirnaamiLekhObj = self.env['nirnaami.lekh.model'].search(
                    [('nirnaami_lekh_related_info_lines.samiti_id.id', '=', rec.id)])

                if len(NirnaamiLekhObj) > 0:
                    rec.nirnaami_lekh_rec = NirnaamiLekhObj
                else:
                    rec.nirnaami_lekh_rec = False

    def _get_book(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                BookObj = self.env['book.model'].search([('samiti_id.id', '=', rec.id)])
                if len(BookObj) > 0:
                    rec.book_rec = BookObj
                else:
                    rec.book_rec = False

    def _get_video(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                VideoObj = self.env['video.model'].search([('samiti_id.id', '=', rec.id)])
                if len(VideoObj) > 0:
                    rec.video_rec = VideoObj
                else:
                    rec.video_rec = False

    def _get_samuday(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                samuday_ids = []

                if rec.samiti_mahatma_id != False and rec.samiti_mahatma_id != None:
                    for mahatma in rec.samiti_mahatma_id:
                        if mahatma.mahatma_id.samuday_id != False and mahatma.mahatma_id.samuday_id != None:
                            for samuday in mahatma.mahatma_id.samuday_id:
                                samuday_ids.append(samuday.id)

                if len(samuday_ids) > 0:
                    rec.samuday_rec = samuday_ids
                else:
                    rec.samuday_rec = False

    name = fields.Char("Samiti Name", required=True)
    description = fields.Text("Description")

    samiti_sr_no = fields.Integer("Sr. No.")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    start_date_vikram_samvant = fields.Char("Start Date Vikram Samvat")
    end_date_vikram_samvant = fields.Char("End Date Vikram Samvat")
    total_members = fields.Integer("Total Members", readonly=True, compute=_get_total_members)
    search_date = fields.Date("Search Date")
    samiti_person_id = fields.One2many('samiti.person', 'ref_field', string="Person")
    samiti_mahatma_id = fields.One2many('samiti.mahatma', 'ref_field', string="Mahatma")
    ref_field = fields.Integer("")
    color = fields.Integer("")

    lekh_rec = fields.One2many('lekh.model', 'lekh_ref_field', string="Lekh", compute=_get_lekh, readonly=True)
    nirnaami_lekh_rec = fields.One2many('nirnaami.lekh.model', 'nirnaami_lekh_ref_field',
                                        string="Nirnaami Lekh", readonly=True, compute=_get_nirnaami_lekh)
    book_rec = fields.One2many('book.model', 'book_ref_field', string="Book", readonly=True, compute=_get_book)
    video_rec = fields.One2many('video.model', 'video_ref_field', string="Video", readonly=True, compute=_get_video)
    samuday_rec = fields.One2many('samuday.model', 'samuday_ref_field', string="Samuday", readonly=True,
                                  compute=_get_samuday)
    rec_state = fields.Selection([('draft', 'Draft'), ('created', 'Created')], default='draft')

    @api.model
    def create(self, values):
        values['rec_state'] = 'created'
        record = super(Samiti, self).create(values)

        return record

    @api.onchange('samiti_mahatma_id')
    def _update_mahatma(self):
        if len(self.samiti_mahatma_id) > 0:
            for mahatma in self.samiti_mahatma_id:
                MahatmaObj = self.env['mahatma.model'].search([('id', '=', mahatma.mahatma_id.id)])
                if len(MahatmaObj) > 0:
                    MahatmaObj.samiti_id = [(0, 0, {'samiti_id': self._origin.id, 'start_date': mahatma.start_date,
                                                    'end_date': mahatma.end_date,
                                                    'start_date_vikram_samvant': mahatma.start_date_vikram_samvant,
                                                    'end_date_vikram_samvant': mahatma.end_date_vikram_samvant})]

    def pass_method(self):
        pass

    def unlink(self):
        for rec in self:
            if rec.samiti_person_id != None and rec.samiti_person_id != False:
                if len(rec.samiti_person_id) > 0:
                    for data in rec.samiti_person_id:
                        SamitiPersonObj = self.env['samiti.person'].search([('id', '=', data.id)])
                        if len(SamitiPersonObj) > 0:
                            SamitiPersonObj.unlink()

            if rec.samiti_mahatma_id != None and rec.samiti_mahatma_id != False:
                if len(rec.samiti_mahatma_id) > 0:
                    for data in rec.samiti_mahatma_id:
                        SamitiMahatmaObj = self.env['samiti.mahatma'].search([('id', '=', data.id)])
                        if len(SamitiMahatmaObj) > 0:
                            SamitiMahatmaObj.unlink()

        return super(Samiti, self).unlink()

    @api.constrains('samiti_sr_no')
    def _check_samiti_sr_no(self):
        if self.samiti_sr_no != False and self.samiti_sr_no != None:
            if len(str(self.samiti_sr_no)) > 11:
                raise ValidationError("Samiti Sr.No. should must be of 11 character Max.")
        lists = []
        SamitiObj = self.env['samiti.model'].search([('id', '!=', self.id)])
        if SamitiObj:
            for rec in SamitiObj:
                lists.append(rec.samiti_sr_no)

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
        if self.samiti_sr_no > 0:
            if self.samiti_sr_no in lists:
                if result == None:
                    raise ValidationError("Sr.No. " + str(
                        self.samiti_sr_no) + " is already taken, You can use any value greater than " + str(
                        lists[-1]) + ".")

                else:
                    raise ValidationError("Sr.No. " + str(self.samiti_sr_no) + " is already taken, You can use '" + str(
                        result) + "' or any value greater than " + str(lists[-1]) + ".")

        else:
            if len(lists) >= 1:
                if result == None:
                    self.samiti_sr_no = lists[-1] + 1
                else:
                    self.samiti_sr_no = result

    @api.constrains('name')
    def _check_name(self):
        if self.name != False and self.name != None:
            if len(self.name) > 100:
                raise ValidationError("Name should must be of 100 character Max.")

    @api.constrains('description')
    def _check_description(self):
        if self.description != False and self.description != None:
            if len(self.description) > 250:
                raise ValidationError("Description should must be of 250 character Max.")
