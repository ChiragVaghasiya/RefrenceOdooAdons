# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class NozzleReadingReport(models.TransientModel):
    _name = 'nozzle.reading.report.wizard'
    _description = 'Nozzle Reading Report'

    report_option = fields.Selection([('by_date', 'By Date'), ('by_balance_report', 'By Balance Report')], 'Print Report')
    start_date = fields.Date('Start Date', default=fields.Date.context_today)
    end_date = fields.Date('End Date', default=fields.Date.context_today)
    balance_report_ids = fields.Many2many('balance.report', string='Balance Report Ids')

    def generate_report(self):
        data = False
        if self.report_option == 'by_date':
            data = {'start_date': self.start_date, 'end_date': self.end_date}
        else: 
            data = {'balance_report_ids': self.balance_report_ids.ids}
        return self.env.ref('fuel_pump_management.nozzle_reading_report').report_action([], data=data)
