from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Samuday(models.Model):
    _name = 'samuday.model'
    _description = 'Samuday'
    _rec_name = 'samuday_name'

    # @api.onchange('samuday_name','paksh_id2','panth_id','link_to_tharav')
    # def _get_gachadhipati(self):
    #     for rec in self:
    #         MahatmaObj = rec.env['mahatma.model'].search([('samuday_id.id','=',rec.self_id),('mahatma_presence','=','yes'),('designation_id','=','gachhadhipati')])
    #         if MahatmaObj:
    #             rec.gachhadhipati_id = MahatmaObj.id
    #             rec.gachhadhipati_date = MahatmaObj.designation_start_date
    #         else:
    #             rec.gachhadhipati_id = None

    def _get_gachhadhipati(self):
        for rec in self:
            MahatmaObj = self.env['mahatma.model'].search(
                [('rec_state', '=', 'created'), ('samuday_id.id', '=', rec.self_id), ('mahatma_presence', '=', 'yes'),
                 ('gachhadhipati', '=', True)],limit=1)
            # if len(MahatmaObj) > 0:
            #     for mahatma in MahatmaObj:
            if MahatmaObj:
                rec.gachhadhipati_of_samuday = MahatmaObj.id
            else:
                rec.gachhadhipati_of_samuday = False

    def _get_self_id(self):
        for rec in self:
            rec.self_id = rec.id

    def _get_mahatma(self):

        for rec in self:

            if rec.id != False and rec.id != None:
                MahatmaObj = self.env['mahatma.model'].search([('samuday_id.id', '=', rec.id)])
                if len(MahatmaObj) > 0:
                    rec.mahatma_rec = MahatmaObj
                else:
                    rec.mahatma_rec = False

    def _get_magazine(self):

        for rec in self:

            if rec.id != False and rec.id != None:
                MagazineObj = self.env['magazine.model'].search([('mahatma_id.samuday_id.id', '=', rec.id)])
                if len(MagazineObj) > 0:
                    rec.magazine_rec = MagazineObj
                else:
                    rec.magazine_rec = False

    def _get_lekh(self):
        for rec in self:
            LekhObj = self.env['lekh.model'].search([('lekh_related_info_lines.samuday_id.id', '=', rec.id)])

            if len(LekhObj) > 0:
                rec.lekh_rec = LekhObj
            else:
                rec.lekh_rec = False

    def _get_nirnaami_lekh(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                NirnaamiLekhObj = self.env['nirnaami.lekh.model'].search(
                    [('nirnaami_lekh_related_info_lines.mahatma_id.samuday_id.id', '=', rec.id)])

                if len(NirnaamiLekhObj) > 0:
                    rec.nirnaami_lekh_rec = NirnaamiLekhObj
                else:
                    rec.nirnaami_lekh_rec = False

    def _get_book(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                BookObj = self.env['book.model'].search([('mahatma_id.samuday_id.id', '=', rec.id)])
                if len(BookObj) > 0:
                    rec.book_rec = BookObj
                else:
                    rec.book_rec = False

    def _get_video(self):
        for rec in self:
            if rec.id != False and rec.id != None:
                VideoObj = self.env['video.model'].search([('mahatma_id.samuday_id.id', '=', rec.id)])
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

    def _get_tharav(self):
        for rec in self:

            if rec.id != False and rec.id != None:

                tharav_ids = []
                TharavObj = self.env['tharav.model'].search([('paksh_id.id', '=', rec.paksh_id2.id)])

                if len(TharavObj) > 0:

                    rec.tharav_rec = TharavObj
                else:
                    rec.tharav_rec = False

    def _get_person(self):

        for rec in self:

            if rec.id != False and rec.id != None:
                PersonObj = self.env['person.model'].search([('mahatma_id.samuday_id.id', '=', rec.id)])
                if len(PersonObj) > 0:
                    rec.person_rec = PersonObj
                else:
                    rec.person_rec = False

    def _get_sanstha(self):

        for rec in self:

            if rec.id != False and rec.id != None:
                SansthaObj = self.env['sanstha.model'].search([('mahatma_id.samuday_id.id', '=', rec.id)])
                if len(SansthaObj) > 0:
                    rec.sanstha_rec = SansthaObj
                else:
                    rec.sanstha_rec = False

    samuday_name = fields.Char("Samuday Name", required=True)
    paksh_id2 = fields.Many2one('paksh.model', "Paksh", required=True)
    panth_id = fields.Selection(
        [('શ્વેતાંબર મૂર્તિપૂજક', 'શ્વેતાંબર મૂર્તિપૂજક'), ('દિગંબર', 'દિગંબર'), ('તેરાપંથ', 'તેરાપંથ'),
         ('સ્થાનકવાસી', 'સ્થાનકવાસી')], "Panth", required=True)
    link_to_tharav = fields.Selection([('none', 'None'), ('one', '1 tithi'), ('two', '2 tithi'), ], "Link to Tharav",
                                      default="none")
    # gachhadhipati_id = fields.Many2one('mahatma.model', "gachhadhipati", compute=_get_gachadhipati)
    gachhadhipati_id = fields.Char("Gachhadhipati")
    gachhadhipati_of_samuday = fields.Many2one('mahatma.model', string="Gachhadhipati", compute=_get_gachhadhipati)
    gachhadhipati_date = fields.Date("Gachhadhipati Start Date")
    self_id = fields.Integer("ID", compute='_get_self_id')
    color = fields.Integer("color")
    samuday_ref_field = fields.Integer("Ref.")

    mahatma_rec = fields.One2many('mahatma.model', 'ref_id', string="Mahatma", readonly=True, compute=_get_mahatma)
    magazine_rec = fields.One2many('magazine.model', 'ref_id', string="Magazine", compute=_get_magazine, readonly=True)
    lekh_rec = fields.One2many('lekh.model', 'lekh_ref_field', string="Lekh", compute=_get_lekh, readonly=True)
    nirnaami_lekh_rec = fields.One2many('nirnaami.lekh.model', 'nirnaami_lekh_ref_field',
                                        string="Nirnaami Lekh", readonly=True, compute=_get_nirnaami_lekh)
    book_rec = fields.One2many('book.model', 'book_ref_field', string="Book", readonly=True, compute=_get_book)
    video_rec = fields.One2many('video.model', 'video_ref_field', string="Video", readonly=True, compute=_get_video)
    tags_rec = fields.Many2many('lekh.tags.model', string="Tag", readonly=True, compute=_get_tags)
    tharav_rec = fields.One2many('tharav.model', 'ref_id', string="Tharav", readonly=True, compute=_get_tharav)
    person_rec = fields.One2many('person.model', 'ref_id', string="Person", readonly=True, compute=_get_person)
    sanstha_rec = fields.One2many('sanstha.model', 'ref_id', string="Sanstha", readonly=True, compute=_get_sanstha)

    @api.model
    def create(self, values):
        record = super(Samuday, self).create(values)

        return record

    @api.constrains('samuday_name')
    def _check_samuday_name(self):
        if len(self.samuday_name) > 175:
            raise ValidationError("Samuday name must be of maximum 175 Characters.")

    def unlink(self):

        for rec in self:
            relations = ""

            MahatmaObj = self.env['mahatma.model'].search([('samuday_id.id', '=', rec.id)])
            if MahatmaObj:
                relations += "Mahatma, "

            LekhObj = self.env['lekh.model'].search([('lekh_related_info_lines.samuday_id.id', '=', rec.id)])
            if LekhObj:
                relations += "Lekh, "

            if relations != "":
                raise ValidationError("You can not delete these record it has relation with " + relations + "model.")

        return super(Samuday, self).unlink()
