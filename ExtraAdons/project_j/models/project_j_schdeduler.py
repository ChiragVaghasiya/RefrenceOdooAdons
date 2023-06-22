from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class ProjectJScheduler(models.Model):
    _name = 'project.j.scheduler'
    _description = 'ProjectJ Scheduler'
    _rec_name = 'scheduler_name'

    # def _get_info(self):
    #     for rec in self:
    #         if (rec.execute_number != None and rec.execute_number != False) and (rec.execute_unit != None and rec.execute_unit != False):
    #             rec.info_line = "This Scheduler will be running at every " + str(rec.execute_number) + " - " + str(rec.execute_unit) + "." 

    scheduler_name = fields.Char("Name", required=True)
    # model_id = fields.Many2one('ir.model', string="Model", default=_get_model)
    # field_id = fields.Many2one('ir.model.fields', string="Field", required=True)
    execute_number = fields.Integer("Execute Number", default=1, required=True)
    execute_unit = fields.Selection(
        [('minutes', 'Minute'), ('hours', 'Hour'), ('days', 'Day'), ('weeks', 'Week'), ('months', 'Month')],
        string="Execute Every", required=True)
    number_of_call = fields.Integer("Number Of Calls", default=-1)
    state = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], default='active', string="Status")
    cron_id = fields.Integer("Cron Id")
    rec_state = fields.Selection([('draft', 'Draft'), ('created', 'Created')], default='draft', string="Rec. State")
    data_list = fields.Char("Data List")
    info_line = fields.Char("Info")

    def actvate_schedular(self):
        self.write({
            'state': 'active',
        })

    def deactivate_schedular(self):
        self.write({
            'state': 'inactive',
        })

    @api.constrains('execute_unit')
    def _check_execute_unit(self):
        for rec in self:
            if rec.execute_unit == None or rec.execute_unit == False:
                raise ValidationError("Please Select Execute Unit")

    @api.onchange('execute_number', 'execute_unit')
    def _update_info_line(self):
        for rec in self:
            rec.info_line = "This Scheduler will be running at every " + str(rec.execute_number) + " - " + str(
                rec.execute_unit) + "."

    @api.model
    def create(self, values):

        if values['execute_unit'] == False or values['execute_unit'] == None:
            raise ValidationError("Please Select Execute Unit")

        vals = {
            'name': values['scheduler_name'],
            'model_id': 410,
            'interval_number': values['execute_number'],
            'interval_type': values['execute_unit'],
            'numbercall': values['number_of_call'],
            'active': True,
        }

        cron_id = self.env['ir.cron'].create(vals)

        values['cron_id'] = cron_id
        values['rec_state'] = 'created'
        values['info_line'] = "This Scheduler will be running at every " + str(values['execute_number']) + " - " + str(
            values['execute_unit']) + "."

        record = super(ProjectJScheduler, self).create(values)

        return record

    def unlink(self):
        for rec in self:
            CronObj = rec.env['ir.cron'].search([('id', '=', rec.cron_id)])
            if CronObj:
                for rec in CronObj:
                    rec.unlink()

        return super(ProjectJScheduler, self).unlink()

    def write(self, vals):

        values = {}

        if 'execute_number' in vals:
            values['interval_number'] = vals['execute_number']

        if 'execute_unit' in vals:
            values['interval_type'] = vals['execute_unit']

        if 'number_of_call' in vals:
            values['numbercall'] = vals['number_of_call']

        if 'state' in vals:
            is_active = True
            if vals['state'] == 'inactive':
                is_active = False

            values['active'] = is_active

        IrCron = self.env['ir.cron'].search([('id', '=', self.cron_id), ('active', '=', (True, False))])
        if IrCron:
            IrCron.write(values)

        # jaofjsfoja
        res = super(ProjectJScheduler, self).write(vals)
        return res

    def due_state_mail_notifier(self):
        MagazineAnkObj = self.env['magazine.ank'].search([('state', '!=', 'completed')])
        for ank in MagazineAnkObj:

            if ank.state == 'due':
                if len(ank.due_date_tracker) > 0:
                    if ank.due_date_tracker[-1].status == 'pending':
                        if (ank.due_date_tracker[-1].date_field + timedelta(days=2)) == datetime.today().date():
                            template_id = self.env.ref('project_j.magazine_ank_is_due_mail_template')
                            mail_id = template_id.send_mail(ank.id, force_send=True)
                            ank.due_date_tracker = [
                                (0, 0, {'date_field': datetime.today().date(), 'status': 'pending'})]

            if ank.state == 'recieved':
                if len(ank.recieved_date_tracker) > 0:
                    if ank.recieved_date_tracker[-1].status == 'pending':
                        if (ank.recieved_date_tracker[-1].date_field + timedelta(days=2)) == datetime.today().date():
                            template_id = self.env.ref('project_j.magazine_ank_recieve_is_due_mail_template')
                            mail_id = template_id.send_mail(ank.id, force_send=True)
                            ank.recieved_date_tracker = [
                                (0, 0, {'date_field': datetime.today().date(), 'status': 'pending'})]

            if ank.state == 'in_review':
                if len(ank.in_review_date_tracker) > 0:
                    if ank.in_review_date_tracker[-1].status == 'pending':
                        if (ank.in_review_date_tracker[-1].date_field + timedelta(days=2)) == datetime.today().date():
                            template_id = self.env.ref('project_j.magazine_ank_review_is_due_mail_template')
                            mail_id = template_id.send_mail(ank.id, force_send=True)
                            ank.in_review_date_tracker = [
                                (0, 0, {'date_field': datetime.today().date(), 'status': 'pending'})]

    def magazine_in_recieved_mail_notifier(self):

        MagazineAnkObj = self.env['magazine.ank'].search([('state', '=', 'recieved')])
        if len(MagazineAnkObj) > 0:

            values = {'magazine_ank_ids': MagazineAnkObj}
            recieved_magazines = self.env['mail.related.model'].create(values)

            MailRelatedInfo = self.env['mail.related.model'].search([('id', '=', recieved_magazines.id)])
            if len(MailRelatedInfo) > 0:
                for rec in MailRelatedInfo:
                    template_id = self.env.ref('project_j.magazine_ank_waiting_for_review_mail_template')
                    mail_id = template_id.send_mail(rec.id, force_send=True)
