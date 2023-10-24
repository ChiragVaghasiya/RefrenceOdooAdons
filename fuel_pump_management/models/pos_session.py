from odoo import models, fields, api

class PosSession(models.Model):
    _inherit = 'pos.session'

    balance_report = fields.Many2one('balance.report', string='Balance Reports')

    def action_pos_session_open(self):
        result = super(PosSession, self).action_pos_session_open()
        # category = self.env['product.category'].search([('name', 'ilike', 'Fuel')], limit=1)
        category = self.env['pos.category'].search([('name', 'ilike', 'Fuel')], limit=1)
        if category and self.config_id.is_nozzle_used and self.company_id == self.config_id.nozzle_company:
            print ('ffff', category)
            categ_id = category.id
            products = self.env['product.product'].search([('pos_categ_id', '=', categ_id)])
            nozzle_products = self.env['pump.pump'].search([('pos_config', '=', self.config_id.id)]).mapped('fuel_type')
            warehouse_id = self.config_id.nozzle_warehouse_id and self.config_id.nozzle_warehouse_id.id
            for product in products:
                if product in nozzle_products:
                    product_start = self.env['product.session.start'].sudo().create({'product_id': product.id, 'warehouse_id': warehouse_id, 'session_id': self.id})
                    print ('FFFFFFFF', product_start)

        return result

    def action_pos_balancing_report(self):
        action_ref = 'fuel_pump_management.action_balance_report'
        action = self.env['ir.actions.act_window']._for_xml_id(action_ref)
        # action['context'] = dict(ast.literal_eval(action.get('context')), default_pump_id=self.id, search_default_pump_id=self.id)
        action['domain'] = [('pos_session', '=', self.id)]
        return action


    def _validate_session(self):
        result = super(PosSession, self)._validate_session()
        if self.config_id.company_id == self.config_id.nozzle_company and self.config_id.is_nozzle_used:
            nozzle_products = self.env['pump.pump'].search([('pos_config', '=', self.config_id.id)]).mapped('fuel_type')
            print ('vvv', nozzle_products)
            list_final_noozle_pro_list = []
            final_nozzles = []
            for order in self.order_ids:
                if order.nozzle_id:
                    for line in order.lines:
                        print (line.product_id, line.qty, line.price_subtotal_incl)
                        if line.product_id in nozzle_products:
                            if order.nozzle_id not in final_nozzles:
                                final_nozzles.append(order.nozzle_id)
                            if list_final_noozle_pro_list:
                                product_include = False
                                for list_final in list_final_noozle_pro_list:
                                    if list_final.get('product_id') == line.product_id.id:
                                        product_include = True
                                        qty = list_final['qty']
                                        price_subtotal_incl = list_final['price_subtotal_incl']
                                        list_final.update({'qty': qty + line.qty})
                                        list_final.update({'price_subtotal_incl': price_subtotal_incl + line.price_subtotal_incl})
                                if not product_include:
                                    final_nozzle_product = {}
                                    final_nozzle_product['product_id'] = line.product_id.id
                                    final_nozzle_product['qty'] = line.qty
                                    final_nozzle_product['price_subtotal_incl'] = line.price_subtotal_incl
                                    # nozzle = self.env['pump.pump'].search([('pos_config', '=', self.config_id.id), ('fuel_type', '=', line.product_id.id)])
                                    # if nozzle not in final_nozzles:
                                    #     final_nozzles.append(nozzle)
                                    list_final_noozle_pro_list.append(final_nozzle_product)
                            else:
                                final_nozzle_product = {}
                                final_nozzle_product['product_id'] = line.product_id.id
                                final_nozzle_product['qty'] = line.qty
                                final_nozzle_product['price_subtotal_incl'] = line.price_subtotal_incl
                                # nozzle = self.env['pump.pump'].search([('pos_config', '=', self.config_id.id), ('fuel_type', '=', line.product_id.id)])
                                # if nozzle not in final_nozzles:
                                #     final_nozzles.append(nozzle)
                                list_final_noozle_pro_list.append(final_nozzle_product)

            print ('Finalllll', list_final_noozle_pro_list, final_nozzles)
            nozzle_1_ids_val = []
            for f_nozzle in final_nozzles:
                nozzle_end = self.env['pump.pump.nozzle'].search([('config_id', '=', self.config_id.id), ('company_id', '=', self.company_id.id), ('pump_id', '=', f_nozzle.id)], order='id desc', limit=1)
                if nozzle_end:
                    nozzle_start_val = {}
                    nozzle_start_val['pump_id'] = f_nozzle.id
                    nozzle_start_val['stage'] = 'opening'
                    nozzle_start_val['pump_rdgs'] = nozzle_end.pump_rdgs
                    nozzle_start_val['pump_rdgl'] = nozzle_end.pump_rdgl
                    nozzle_start_val['pump_rdg_side'] = nozzle_end.pump_rdg_side
                    nozzle_1_ids_val.append((0,0, nozzle_start_val))
                else:
                    nozzle_start_val = {}
                    nozzle_start_val['pump_id'] = f_nozzle.id
                    nozzle_start_val['stage'] = 'opening'
                    nozzle_start_val['pump_rdgs'] = 0.0
                    nozzle_start_val['pump_rdgl'] = 0.0
                    nozzle_start_val['pump_rdg_side'] = 0.0
                    nozzle_1_ids_val.append((0,0, nozzle_start_val))
                nozzle_end_val = {}
                nozzle_end_val['pump_id'] = f_nozzle.id
                nozzle_end_val['stage'] = 'closing'
                nozzle_end_val['pump_rdgs'] = 0.0
                nozzle_end_val['pump_rdgl'] = 0.0
                nozzle_end_val['pump_rdg_side'] = 0.0
                nozzle_1_ids_val.append((0,0, nozzle_end_val))

            print ('TYYTYTYT', nozzle_1_ids_val)
            balance_rep_pro_session_ids_val = []
            sales_by_product_ids_val = []
            for final_pro in list_final_noozle_pro_list:
                final_pro_val = {}
                final_pro_sale_val = {}
                if final_pro.get('product_id'):
                    final_pro_val['product_id'] = final_pro.get('product_id')
                    final_pro_sale_val['product_id'] = final_pro.get('product_id')
                    start_qty_available = self.env['product.session.start'].search([('session_id', '=', self.id), ('product_id', '=', final_pro.get('product_id'))], limit=1)
                    final_pro_val['litre_in_tank_start'] = start_qty_available.qty_availablae
                    warehouse_id = self.config_id.nozzle_warehouse_id and self.config_id.nozzle_warehouse_id.id
                    # picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('company_id', '=', self.company_id.id)])
                    # move_lines = self.env['stock.move'].search([('product_id', '=', final_pro.get('product_id')), ('state', '=', 'done'), ('write_date', '>=', self.start_at), ('write_date', '>=', self.stop_at), ('picking_type_id', 'in', picking_type.ids)])
                    # purchase_qty = 0.0
                    # for move in move_lines:
                    #     purchase_qty += product_qty
                    stock_at_end = self.env['product.product'].browse(final_pro.get('product_id')).with_context(warehouse=self.config_id.nozzle_warehouse_id.id, fuel_pump=True).qty_available 
                    final_pro_val['stock_at_end_session'] = stock_at_end
                    # final_pro_val['purchase_qty'] = purchase_qty
                    final_pro_val['sale_qty_session'] = final_pro.get('qty')
                    final_pro_val['sales_dollar_session'] = final_pro.get('price_subtotal_incl')
                    balance_rep_pro_session_ids_val.append((0,0, final_pro_val))
                    sales_by_product_ids_val.append((0,0, final_pro_sale_val))

            print ('qqqqTYYTYTYT', nozzle_1_ids_val)
            date_stop = self.stop_at.strftime('%m/%d/%Y')
            balance_report_vals = {'name': date_stop + '-' + self.name + '-' + self.user_id.name,
                                    'pos_session': self.id,
                                    'user_id': self.user_id.id,
                                    'date': self.stop_at.date(),
                                    'company_id': self.company_id.id,
                                    'nozzle_1_ids': nozzle_1_ids_val,
                                    'balance_rep_pro_session_ids': balance_rep_pro_session_ids_val,
                                    'sales_by_product_ids': sales_by_product_ids_val}
            report = self.env['balance.report'].create(balance_report_vals)
            print ('ttt', report)
        return result