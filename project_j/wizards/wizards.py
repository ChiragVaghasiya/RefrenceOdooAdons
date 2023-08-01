from odoo import models, fields, api


class MessageWizard(models.TransientModel):
    _name = 'message.wizard'
    _description = 'Message Wizard'

    message = fields.Text('Message', readonly=True)
    mahatma_id = fields.One2many('mahatma.model', 'ref_id', string="Mahatma", readonly=True)
    magazine_id = fields.One2many('magazine.model', 'ref_id', string="Magazine", readonly=True)
    lekh_id = fields.One2many('lekh.model', 'lekh_ref_field', string="Lekh", readonly=True)
    nirnaami_lekh_id = fields.One2many('nirnaami.lekh.model', 'nirnaami_lekh_ref_field', string="Nirnaami Lekh",
                                       readonly=True)
    book_id = fields.One2many('book.model', 'book_ref_field', string="Book", readonly=True)
    video_id = fields.One2many('video.model', 'video_ref_field', string="Video", readonly=True)
    display_model = fields.Char("")
    display_flag = fields.Boolean("")

    def action_ok(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}


class SearchName(models.TransientModel):
    _name = 'search.name'
    _description = 'Search Name'

    name = fields.Char("Name")

    def save_record(self):
        if self._context['active_model'] == 'advance.search.result':
            type_of_result = 'doc'

            WizResult = self.env['advance.search.result'].search([('id', '=', self._context['active_id'])])
            results_list = []
            if len(WizResult) > 0:
                for results in WizResult.document_ids:
                    results_list.append((4, results.id))

            if not len(results_list) > 0:
                results_list = False

            self.env['advance.search.results.model'].create({
                'name': self.name,
                'result_type': 'doc',
                'doc_ids': results_list, })

        elif self._context['active_model'] == 'magazine.model':
            type_of_result = 'magazine'

            WizResult = self.env['magazine.model'].search([('id', '=', self._context['active_ids'])])
            results_list = []
            if len(WizResult) > 0:
                for results in WizResult:
                    results_list.append((4, results.id))

            if not len(results_list) > 0:
                results_list = False

            self.env['advance.search.results.model'].create({
                'name': self.name,
                'result_type': 'magazine',
                'magazine_ids': results_list, })
