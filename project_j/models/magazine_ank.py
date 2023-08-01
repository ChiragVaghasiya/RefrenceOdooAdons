from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


class SchedulerDateTracker(models.Model):
    _name = 'scheduler.date.tracker'
    _description = 'Scheduler Date Tracker'

    date_field = fields.Date("Date")
    status = fields.Selection([('pending', 'Pending'), ('done', 'Done')], "Status")
    ref_field = fields.Integer("")


class MagazineAnk(models.Model):
    _name = 'magazine.ank'
    _description = 'Magazine Ank'

    # _rec_name = 'lekh_tag_name'

    def _get_magazines(self):
        domain = []
        MagazineObj = self.env['magazine.model'].search([('monitor_for_abusive_contents', '=', True)])
        if MagazineObj:
            for rec in MagazineObj:
                domain.append(rec.id)

        return domain

    @api.onchange('publication_date')
    def _get_ank_number(self):
        if self.publication_date:
            self.ank_number = datetime.strftime(self.publication_date, '%b-%Y')

    ank_name = fields.Char("Ank Name", required=True)
    ank_number = fields.Char("Ank Number", required=True, readonly=True)
    publication_date = fields.Date("Publication Date", required=True)
    magazine_id = fields.Many2one('magazine.model', string="Magazine", required=True)
    state = fields.Selection([
        ('due', 'Due'),
        ('recieved', 'Recieved'),
        ('in_review', 'In Review'),
        ('completed', 'Completed'),
    ], string="Status", default='due')

    fix_email = fields.Char("", default="sagar.panchal@aspiresoftserv.com")
    email = fields.Char("", default="sempanchal123@gmail.com")

    due_date_tracker = fields.One2many('scheduler.date.tracker', 'ref_field', category_ids='due',
                                       string="Due Date Tracker")
    recieved_date_tracker = fields.One2many('scheduler.date.tracker', 'ref_field', category_ids='recieved',
                                            string="Recieved Date Tracker")
    in_review_date_tracker = fields.One2many('scheduler.date.tracker', 'ref_field', category_ids='in_review',
                                             string="In Review Date Tracker")
    ref_field = fields.Integer("")

    def magazine_ank_recieved(self):

        template_id = self.env.ref('project_j.magazine_ank_recieved_mail_template')
        mail_id = template_id.send_mail(self.id, force_send=True)

        self.write({
            'state': 'recieved',
            'due_date_tracker': [(0, 0, {'date_field': datetime.today().date(), 'status': 'done'})],
            'recieved_date_tracker': [(0, 0, {'date_field': datetime.today().date(), 'status': 'pending'})]

        })

    def magazine_ank_in_review(self):

        template_id = self.env.ref('project_j.magazine_ank_in_review_mail_template')
        mail_id = template_id.send_mail(self.id, force_send=True)

        self.write({
            'state': 'in_review',
            'recieved_date_tracker': [(0, 0, {'date_field': datetime.today().date(), 'status': 'done'})],
            'in_review_date_tracker': [(0, 0, {'date_field': datetime.today().date(), 'status': 'pending'})]
        })

    def magazine_ank_completed(self):

        template_id = self.env.ref('project_j.magazine_ank_completed_mail_template')
        mail_id = template_id.send_mail(self.id, force_send=True)

        self.write({
            'state': 'completed',
            'in_review_date_tracker': [(0, 0, {'date_field': datetime.today().date(), 'status': 'done'})]
        })

    # def due_state_mail_notifier(self):
    #     MagazineAnkObj = self.env['magazine.ank'].search([('state','!=','completed')])
    #     for ank in MagazineAnkObj:

    #         if ank.state == 'due':
    #             if len(ank.due_date_tracker) > 0:
    #                 if ank.due_date_tracker[-1].status == 'pending':
    #                     if (ank.due_date_tracker[-1].date_field + timedelta(days=2)) == datetime.today().date():
    #                         template_id = self.env.ref('project_j.magazine_ank_is_due_mail_template')
    #                         mail_id = template_id.send_mail(ank.id, force_send=True)                
    #                         ank.due_date_tracker = [(0, 0, {'date_field':datetime.today().date(), 'status': 'pending'})]

    #         if ank.state == 'recieved':
    #             if len(ank.recieved_date_tracker) > 0:
    #                 if ank.recieved_date_tracker[-1].status == 'pending':
    #                     if (ank.recieved_date_tracker[-1].date_field + timedelta(days=2)) == datetime.today().date():
    #                         template_id = self.env.ref('project_j.magazine_ank_recieve_is_due_mail_template')
    #                         mail_id = template_id.send_mail(ank.id, force_send=True)                
    #                         ank.recieved_date_tracker = [(0, 0, {'date_field':datetime.today().date(), 'status': 'pending'})]

    #         if ank.state == 'in_review':
    #             if len(ank.in_review_date_tracker) > 0:
    #                 if ank.in_review_date_tracker[-1].status == 'pending':
    #                     if (ank.in_review_date_tracker[-1].date_field + timedelta(days=2)) == datetime.today().date():
    #                         template_id = self.env.ref('project_j.magazine_ank_review_is_due_mail_template')
    #                         mail_id = template_id.send_mail(ank.id, force_send=True)                
    #                         ank.in_review_date_tracker = [(0, 0, {'date_field':datetime.today().date(), 'status': 'pending'})]

    @api.model
    def create(self, values):

        if 'publication_date' in values:
            values['ank_number'] = datetime.strftime(
                datetime.strptime(values['publication_date'], DEFAULT_SERVER_DATE_FORMAT), '%b-%Y')

        values['due_date_tracker'] = [(0, 0, {'date_field': datetime.today().date(), 'status': 'pending'})]

        record = super(MagazineAnk, self).create(values)

        template_id = self.env.ref('project_j.magazine_ank_created_mail_template')
        mail_id = template_id.send_mail(record.id, force_send=True)

        return record
