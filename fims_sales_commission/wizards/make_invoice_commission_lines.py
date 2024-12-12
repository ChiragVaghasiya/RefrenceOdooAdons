# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
from odoo import models, fields, api, exceptions

class Wizard(models.TransientModel):
    _name = 'commission.lines.create.inv'
    _description = 'commission lines create inv'

    def _default_get_ids(self):
        return self.env['commission.lines'].browse(self._context.get('active_ids'))

    active_ids = fields.Many2many('commission.lines', default=_default_get_ids, invisible=True)
    group_by = fields.Boolean(string="Group BY")

    def create_invoice(self):
        if self.group_by:
            self._create_invoice()
        else:
            invoice = ''
            for id in self.active_ids:
                AccountInvoice = self.env['account.move']
                ICPSudo = self.env['ir.config_parameter'].sudo()
                commission_expense_account_id = int(ICPSudo.get_param('fims_sales_commission.commission_expense_account_id'))
                if not commission_expense_account_id:
                    raise exceptions.ValidationError("Please set Commission Expense Account from Sales/Configuration/Setting/Sales Commission.")
                if not id.invoice_id:
                    invoice = AccountInvoice.create({
                        'move_type': 'in_invoice',
                        'partner_id': id.sales_person_partner_id.id,
                        'invoice_date': fields.Date.today(),
                        'invoice_line_ids': [(0, 0, {
                            'name': id.description + "/" + (id.order_reference or id.invoice_reference),
                            'account_id': commission_expense_account_id,
                            'price_unit': id.commission_amount,
                            'price_subtotal': id.commission_amount,
                        })]
                    })
                    id.invoice_id = invoice.id
            return invoice

    def _create_invoice(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        commission_expense_account_id = int(ICPSudo.get_param('fims_sales_commission.commission_expense_account_id'))
        if not commission_expense_account_id:
            raise exceptions.ValidationError("Please set Commission Expense Account from Sales/Configuration/Setting/Sales Commission.")
        commission_lines = self.env['commission.lines'].read_group([('id', 'in', self.env.context.get('active_ids'))],
                                                          ['description', 'order_reference', 'invoice_reference', 'commission_amount', 'user_id'],
                                                          'user_id')
        for commission_line in commission_lines:
            domain = commission_line['__domain']
            domain.append(('invoice_id', '=', False))
            lines = self.env['commission.lines'].search(domain)
            AccountInvoice = self.env['account.move']
            if lines:
                inv_lines = []
                for line in lines:
                    line_vals = {
                            'name': line.description + "/" + (line.order_reference or line.invoice_reference),
                            'account_id': commission_expense_account_id,
                            'price_unit': line.commission_amount,
                            'price_subtotal': line.commission_amount}
                    inv_lines.append((0, 0, line_vals))

                inv_obj = AccountInvoice.create({
                    'move_type': 'in_invoice',
                    'partner_id': lines[0].sales_person_partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': inv_lines
                })
                lines.invoice_id = inv_obj.id
