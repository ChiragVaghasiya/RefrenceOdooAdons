from odoo import models, fields, api, _
from odoo.exceptions import UserError

from lxml import etree



class BalanceReport(models.Model):
    _name = 'balance.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Balance Report"
    

    def _get_default_stage(self):
        state = self.env.ref('fuel_pump_management.balance_report_stage_draft', raise_if_not_found=False)
        return state if state and state.id else False

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['balance.report.stage'].search([], order=order)


    @api.depends('total_sale_in_dollar', 'total_on_sales_receipt')
    def get_difference(self):
        self.difference = self.total_sale_in_dollar - self.total_on_sales_receipt

    @api.depends('sales_by_product_ids', 'sales_by_product_ids.product_difference')
    def is_difference_on_product_stock(self):
        if any(line.product_difference != 0  for line in self.sales_by_product_ids):
            self.is_difference_on_product = True
        else:
            self.is_difference_on_product = False

    # def is_stock_adjust_user(self):
    #     user_id = self.env.uid
    #     print ('user_id', self.env.uid)
    #     user = self.env['res.users'].browse(user_id)
    #     if user.is_applicable_stock_adjust_pos:
    #         self.stock_adjustment = True
    #     else:
    #         self.stock_adjustment = False


    name = fields.Char('Name', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    date = fields.Date('Date')
    pos_session = fields.Many2one('pos.session', 'POS')
    user_id = fields.Many2one('res.users', 'Supervisor', related='pos_session.user_id', store=True)
    # state = fields.Selection([('draft', 'Draft'), ('superviser_approved', 'Superviser Approved'), ('approved', 'Approved'), ('confirmed', 'Confirmed')], 'Stage')
    stage_id = fields.Many2one('balance.report.stage', string='Stage', ondelete='set null', default=_get_default_stage, group_expand='_read_group_stage_ids', tracking=True)
    
    pump_id = fields.Many2one('pump.pump', string='Fuel Pump')
    currency_id = fields.Many2one('res.currency', related='pos_session.currency_id', string="Currency", readonly=True)
    
    nozzle_1_ids = fields.One2many('pump.pump.nozzle', 'balance_report_id', 'Nozzles Reading')
    # nozzle_2_ids = fields.One2many('nozzle.2', 'balance_report_id', 'Nozzle 2')
    balance_rep_pro_session_ids = fields.One2many('balance.report.product.session', 'balance_report_id', string='Product Balance Sessions')

    total_sale_in_liter = fields.Float('Sales In Litre Pump', compute='get_compute_from_nozzle_reading')
    total_sale_in_dollar = fields.Monetary('Sales In Dollars Pump', currency_field='currency_id', compute='get_compute_from_nozzle_reading')
    avg_retail = fields.Float('Average Retail', compute='get_compute_from_nozzle_reading')
    total_on_sales_receipt = fields.Monetary('Total on Sales Receipt', compute='get_total_dollar_from_session')
    difference = fields.Monetary('Difference', compute='get_difference')

    sales_by_product_ids = fields.One2many('balance.product.sales', 'balance_report_id', string='Total Sales by Product')
    # stock_adjustment = fields.Boolean('Is applicable Adjustment', compute='is_stock_adjust_user')
    is_difference_on_product = fields.Boolean('Is Difference on Stock', compute='is_difference_on_product_stock', store=True)
    # balancing_report_type = fields.Selection([('station_supervisor', 'Station Supervisor'), ('back_office_supervisor', 'Back Office Supervisor'), ('master_supervisor', 'Master Supervisor')], 'Report Type', compute="_comoute_balancing_report_type")

    # @api.depends('company_id')
    # def _comoute_balancing_report_type(self):
    #     for rec in self:
    #         if self.env.user.has_group('fuel_pump_management.group_master_supervisor'):
    #             rec.balancing_report_type = 'master_supervisor'

    @api.depends('balance_rep_pro_session_ids.sales_dollar_session')
    def get_total_dollar_from_session(self):
        self.total_on_sales_receipt = 0.0
        if self.balance_rep_pro_session_ids:
            self.total_on_sales_receipt = sum(product_balance.sales_dollar_session for product_balance in self.balance_rep_pro_session_ids)

    @api.depends('nozzle_1_ids.pump_rdgl', 'nozzle_1_ids.pump_rdgs')
    def get_compute_from_nozzle_reading(self):
        self.total_sale_in_liter = 0.0
        self.total_sale_in_dollar = 0.0
        self.avg_retail = 0.0
        if self.nozzle_1_ids:
            opening_total_litre = sum(nozzle_reading.pump_rdgl for nozzle_reading in self.nozzle_1_ids.filtered(lambda l: l.stage == 'opening'))
            closing_total_litre = sum(nozzle_reading.pump_rdgl for nozzle_reading in self.nozzle_1_ids.filtered(lambda l: l.stage == 'closing'))
            self.total_sale_in_liter = closing_total_litre - opening_total_litre
            opening_total_price = sum(nozzle_reading.pump_rdgs for nozzle_reading in self.nozzle_1_ids.filtered(lambda l: l.stage == 'opening'))
            closing_total_price = sum(nozzle_reading.pump_rdgs for nozzle_reading in self.nozzle_1_ids.filtered(lambda l: l.stage == 'closing'))
            self.total_sale_in_dollar = closing_total_price - opening_total_price
            if self.total_sale_in_liter > 0:
                self.avg_retail = self.total_sale_in_dollar / self.total_sale_in_liter

    @api.onchange('stage_id')
    def onchnage_stage(self):
        if not self.env.user.has_group('fuel_pump_management.group_station_supervisor') and self.stage_id.name == 'Supervisor Approved':
            raise UserError(_('Only Station Supervisor can Approved'))
        if not self.env.user.has_group('fuel_pump_management.group_back_office_supervisor') and self.stage_id.name == 'Approved':
            raise UserError(_('Only Back Office Supervisor can Approved'))
        if not self.env.user.has_group('fuel_pump_management.group_master_supervisor') and self.stage_id and self.stage_id.name == 'Confirmed':
            raise UserError(_('Only Master Supervisor can Approved'))

    def action_stock_adjustment(self):
        context = dict(self.env.context or {})
        product_ids = []
        location_ids = []
        for product_sale in self.sales_by_product_ids:
            if product_sale.product_difference != 0:
                product_ids.append(product_sale.product_id.id)
        location = self.pos_session.config_id.nozzle_warehouse_id and self.pos_session.config_id.nozzle_warehouse_id.lot_stock_id
        if location:
            location_ids.append(location.id)
        context['default_name'] = self.name
        context['default_product_ids'] = product_ids
        context['default_company_id'] = self.company_id.id
        context['default_location_ids'] = location_ids
        context['default_company_id'] = self.company_id.id
        action = {
                'name': self.name or _('Stock Adjustment'),
                'view_mode': 'form',
                'res_model': 'stock.inventory',
                'view_id': self.env.ref('stock.view_inventory_form').id,
                'type': 'ir.actions.act_window',
                'context': context,
                'target': 'current'
            }

        return action



    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(BalanceReport, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                      submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['fields']['nozzle_1_ids']['views']['tree']['arch'])
            node = doc.xpath("//field[@name='pump_rdgs']")[0]
            node1 = doc.xpath("//field[@name='pump_rdgl']")[0]
            node2 = doc.xpath("//field[@name='pump_rdg_side']")[0]
            if self.env.user.has_group('fuel_pump_management.group_master_supervisor'):
                node.set('modifiers', '{"readonly": false}')
                node1.set('modifiers', '{"readonly": false}')
                node2.set('modifiers', '{"readonly": false}')

            res['fields']['nozzle_1_ids']['views']['tree']['arch'] = etree.tostring(doc)
        
        return res



class BalanceRepotProductSession(models.Model):
    _name = 'balance.report.product.session'
    _description = ' Balance Report by POS Session for Product'

    @api.depends('litre_in_tank_start', 'purchase_qty', 'sale_qty_session')
    def get_balance(self):
        for rec in self:
            rec.balance = rec.litre_in_tank_start + rec.purchase_qty - rec.sale_qty_session

    def get_available_qty(self):
        for rec in self:
            rec.stock_at_end = 0.0
            if rec.config_id.nozzle_warehouse_id:
                rec.stock_at_end = rec.product_id.with_context(
                    warehouse=rec.config_id.nozzle_warehouse_id.id
                ).qty_available

    @api.depends('sale_qty_session', 'litre_in_tank_start', 'stock_at_end_session')
    def get_purchase_qty(self):
        for rec in self:
            rec.purchase_qty = 0.0
            rec.purchase_qty =  rec.stock_at_end_session + rec.sale_qty_session - rec.litre_in_tank_start


    @api.depends('stock_at_end', 'balance')
    def get_actual_diff(self):
        for rec in self:
            rec.over_shot = rec.stock_at_end - rec.balance

    


    pump_id = fields.Many2one('pump.pump', string='Nozzle')
    balance_report_id = fields.Many2one('balance.report', string='Report')
    session_id = fields.Many2one('pos.session', string='POS Session', related='balance_report_id.pos_session')
    config_id = fields.Many2one('pos.config', string='Config', related='session_id.config_id')
    company_id = fields.Many2one('res.company', related='session_id.company_id', string="Company", readonly=True)
    currency_id = fields.Many2one('res.currency', related='session_id.currency_id', string="Currency", readonly=True)
    product_id = fields.Many2one('product.product', string='Product')
    litre_in_tank_start = fields.Float('Litres in tank at start', default=0.0)
    purchase_qty = fields.Float('Purchase during Session', compute='get_purchase_qty')
    sale_qty_session = fields.Float('Sales Qty on Session', default=0.0)
    sales_dollar_session = fields.Monetary('Sales Dollar in Session', currency_field='currency_id')
    balance = fields.Float('Balance', compute='get_balance')
    stock_at_end_session = fields.Float('Stock At End of Session')
    stock_at_end = fields.Float('Stock At End')
    over_shot = fields.Float('Over/Shot', compute='get_actual_diff')


# class BalanceReportProductUser(models.Model):
#     _name = 'balance.report.product.user'

#     def get_avg_retail(self):
#         if self.total_sale_in_liter > 0:
#             self.get_avg_retail = self.total_sale_in_dollar / self.total_sale_in_liter

#     pump_id = fields.Many2one('pump.pump', string='Nozzle')
#     balance_report_id = fields.Many2one('balance.report', string='Report')
#     session_id = fields.Many2one('pos.session', string='POS Session', related='balance_report_id.pos_session')
#     company_id = fields.Many2one('res.company', related='session_id.company_id', string="Company", readonly=True)
#     currency_id = fields.Many2one('res.currency', related='session_id.currency_id', string="Currency", readonly=True)
#     product_id = fields.Many2one('product.product', string='Product')
#     sales_in_litre = fields.Float('Sales in Litre')
#     sales_in_dollar = fields.Monetary('Sales in Dollar', currency_field='currency_id')
#     avg_retail = fields.Float('Average Retail', compute='get_avg_retail')

class BalanceReportProductSale(models.Model):
    _name = 'balance.product.sales'
    _description = 'Total Sales by Product in Balance Report'

    product_id = fields.Many2one('product.product', string='Product')
    balance_report_id = fields.Many2one('balance.report', string='Balance Report')
    currency_id = fields.Many2one('res.currency', related='balance_report_id.pos_session.currency_id', string="Currency", readonly=True)
    product_sales_in_liter = fields.Float('Sales In Litre Pump', compute='get_compute_from_product_nozzle_reading')
    product_sale_in_dollar = fields.Monetary('Sales In Dollars Pump', currency_field='currency_id', compute='get_compute_from_product_nozzle_reading')
    product_avg_retail = fields.Float('Average Retail', compute='get_compute_from_product_nozzle_reading')
    product_on_sales_receipt = fields.Monetary('Total on Sales Receipt', compute='get_total_dollar_from_product_session')
    product_difference = fields.Monetary('Difference', compute='get_difference_product')

    @api.depends('product_sale_in_dollar', 'product_on_sales_receipt')
    def get_difference_product(self):
        for rec in self:
            rec.product_difference = rec.product_sale_in_dollar - rec.product_on_sales_receipt


    @api.depends('balance_report_id.balance_rep_pro_session_ids.sales_dollar_session', 'product_id')
    def get_total_dollar_from_product_session(self):
        for rec in self:
            rec.product_on_sales_receipt = 0.0
            if rec.balance_report_id and rec.balance_report_id.balance_rep_pro_session_ids and rec.product_id:
                product_on_sales_receipt = 0.0
                for product_balance in rec.balance_report_id.balance_rep_pro_session_ids:
                    if product_balance.product_id == rec.product_id:
                        product_on_sales_receipt += product_balance.sales_dollar_session
                rec.product_on_sales_receipt = product_on_sales_receipt

    @api.depends('balance_report_id.nozzle_1_ids.pump_rdgl', 'balance_report_id.nozzle_1_ids.pump_rdgs', 'product_id')
    def get_compute_from_product_nozzle_reading(self):
        for rec in self:
            rec.product_sales_in_liter = 0.0
            rec.product_sale_in_dollar = 0.0
            rec.product_avg_retail = 0.0
            if rec.balance_report_id and rec.balance_report_id.nozzle_1_ids and rec.product_id:
                opening_total_litre = sum(nozzle_reading.pump_rdgl for nozzle_reading in rec.balance_report_id.nozzle_1_ids.filtered(lambda l: l.stage == 'opening' and l.pump_id.fuel_type == rec.product_id))
                closing_total_litre = sum(nozzle_reading.pump_rdgl for nozzle_reading in rec.balance_report_id.nozzle_1_ids.filtered(lambda l: l.stage == 'closing' and l.pump_id.fuel_type == rec.product_id))
                rec.product_sales_in_liter = closing_total_litre - opening_total_litre
                opening_total_price = sum(nozzle_reading.pump_rdgs for nozzle_reading in rec.balance_report_id.nozzle_1_ids.filtered(lambda l: l.stage == 'opening' and l.pump_id.fuel_type == rec.product_id))
                closing_total_price = sum(nozzle_reading.pump_rdgs for nozzle_reading in rec.balance_report_id.nozzle_1_ids.filtered(lambda l: l.stage == 'closing' and l.pump_id.fuel_type == rec.product_id))
                rec.product_sale_in_dollar = closing_total_price - opening_total_price
                if rec.product_sales_in_liter > 0:
                    rec.product_avg_retail = rec.product_sale_in_dollar / rec.product_sales_in_liter


    