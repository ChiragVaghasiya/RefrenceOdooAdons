# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ReportNozzleReadings(models.AbstractModel):
    _name = 'report.fuel_pump_management.report_nozzle_readings'
    _description = 'Report Nozzle Readings'

    @api.model
    def _get_report_values(self, docids, data=None):
        balance_ids = False
        if data.get('balance_report_ids'):
            balance_ids = self.env['balance.report'].browse(data.get('balance_report_ids'))
        else:
            balance_ids = self.env['balance.report'].search([('date', '>=', data.get('start_date')), ('date', '<=', data.get('end_date'))])

        # Nozzle Unique Data
        pump_ids = []
        nozzle_bifercate_id = []
        for nozzle in balance_ids.nozzle_1_ids:
            pump = nozzle.pump_id
            if pump.id not in pump_ids:
                # Pump Opening Rec with min Open session time
                open_nozzles = balance_ids.nozzle_1_ids.filtered(lambda l: l.pump_id.id == pump.id and l.stage == 'opening')
                open_session_id = open_nozzles.session_id.sorted(key=lambda r: r.start_at)
                if open_session_id:
                    open_rec = open_nozzles.filtered(lambda l: l.session_id.id == open_session_id[0].id).sorted(key=lambda r: r.id)
                    if open_rec:
                        nozzle_bifercate_id.append(open_rec[0])

                # Pump Closing Rec with last Close session time
                close_nozzles = balance_ids.nozzle_1_ids.filtered(lambda l: l.pump_id.id == pump.id and l.stage == 'closing')
                close_session_id = close_nozzles.session_id.sorted(key=lambda r: r.stop_at)
                if close_session_id:
                    close_rec = close_nozzles.filtered(lambda l: l.session_id.id == close_session_id[-1].id).sorted(key=lambda r: r.id)
                    if close_rec:
                        nozzle_bifercate_id.append(close_rec[-1])
                pump_ids.append(pump.id)
        

        #generate total_product sale from session in and session out record.
        nozzle_bifercate_id_record = []
        for nozzle in nozzle_bifercate_id:
            nozzle_bifercate_id_record.append(nozzle.id)

        total_product_sales_dict = {}
        nozzle_bifercate_id_record_data = self.env['pump.pump.nozzle'].browse(nozzle_bifercate_id_record)


        for nozzle_total in nozzle_bifercate_id_record_data:
            if nozzle_total.pump_id.name in total_product_sales_dict:
                pass
            else:
                total_data_record = nozzle_bifercate_id_record_data.filtered(lambda l: l.pump_id == nozzle_total.pump_id)
                total_data_record_ordered = total_data_record.sorted(key=lambda r: r.pump_rdgs)
                
                nozzle_dict = {
                    'product_sale_in_dollar' : total_data_record_ordered[1].pump_rdgs - total_data_record_ordered[0].pump_rdgs,
                    'product_sales_in_liter' : total_data_record_ordered[1].pump_rdgl - total_data_record_ordered[0].pump_rdgl
                }
                total_product_sales_dict[nozzle_total.pump_id.name] = nozzle_dict


        total_product_sales_replica_pump = {}
        for product in total_product_sales_dict:

            pump_id = self.env['pump.pump'].search([('name','=',product)])
            product_name = pump_id.fuel_type

            if product_name in total_product_sales_replica_pump:
                nozzle_dict = {
                    'product_sale_in_dollar' :total_product_sales_replica_pump[product_name]['product_sale_in_dollar'] + total_product_sales_dict[product]['product_sale_in_dollar'],
                    'product_sales_in_liter' : total_product_sales_replica_pump[product_name]['product_sales_in_liter'] + total_product_sales_dict[product]['product_sales_in_liter']
                }
            else:
                nozzle_dict = {
                    'product_sale_in_dollar' :total_product_sales_dict[product]['product_sale_in_dollar'],
                    'product_sales_in_liter' :total_product_sales_dict[product]['product_sales_in_liter'],
                }

            total_product_sales_replica_pump[product_name] = nozzle_dict

        # Total Product Sales
        total_product_sales =  [{'product': rec,\
                'product_sales_in_liter': sum(balance_ids.sales_by_product_ids.filtered(lambda l: l.product_id == rec).mapped('product_sales_in_liter')),\
                'product_sale_in_dollar': sum(balance_ids.sales_by_product_ids.filtered(lambda l: l.product_id == rec).mapped('product_sale_in_dollar')),\
                'product_avg_retail': sum(balance_ids.sales_by_product_ids.filtered(lambda l: l.product_id == rec).mapped('product_avg_retail')),\
                'product_on_sales_receipt': sum(balance_ids.sales_by_product_ids.filtered(lambda l: l.product_id == rec).mapped('product_on_sales_receipt')),\
                'product_difference': sum(balance_ids.sales_by_product_ids.filtered(lambda l: l.product_id == rec).mapped('product_difference')),\
                } for rec in balance_ids.sales_by_product_ids.mapped('product_id') if balance_ids.sales_by_product_ids]


        for total_product in total_product_sales:
            if total_product['product'] in total_product_sales_replica_pump:
                total_product['product_sale_in_dollar'] = total_product_sales_replica_pump[total_product['product']]['product_sale_in_dollar']
                total_product['product_sales_in_liter'] = total_product_sales_replica_pump[total_product['product']]['product_sales_in_liter']
                total_product['product_difference'] = total_product['product_sale_in_dollar'] - total_product['product_on_sales_receipt']
                total_product['product_avg_retail'] = total_product['product_sale_in_dollar'] / total_product['product_sales_in_liter']


        # Nozzle Reading by POS Session
        nozzle_reading_by_pos_session =  [{'product': rec,\
                'litre_in_tank_start': round(balance_ids.balance_rep_pro_session_ids.filtered(lambda l: l.product_id == rec).mapped('litre_in_tank_start')[0],3),\
                'purchase_qty': round(sum(balance_ids.balance_rep_pro_session_ids.filtered(lambda l: l.product_id == rec).mapped('purchase_qty')),3),\
                'sale_qty_session': round(sum(balance_ids.balance_rep_pro_session_ids.filtered(lambda l: l.product_id == rec).mapped('sale_qty_session')),3),\
                'sales_dollar_session': round(sum(balance_ids.balance_rep_pro_session_ids.filtered(lambda l: l.product_id == rec).mapped('sales_dollar_session')),3),\
                # 'balance': round(sum(balance_ids.balance_rep_pro_session_ids.filtered(lambda l: l.product_id == rec).mapped('balance')),3),\
                'balance':round(balance_ids.balance_rep_pro_session_ids.filtered(lambda l: l.product_id == rec).mapped('litre_in_tank_start')[0] + sum(balance_ids.balance_rep_pro_session_ids.filtered(lambda l: l.product_id == rec).mapped('purchase_qty')) - sum(balance_ids.balance_rep_pro_session_ids.filtered(lambda l: l.product_id == rec).mapped('sale_qty_session')),3),\
                'stock_at_end': round(balance_ids.balance_rep_pro_session_ids.filtered(lambda l: l.product_id == rec).mapped('stock_at_end')[-1],3),\
                'over_shot': round(sum(balance_ids.balance_rep_pro_session_ids.filtered(lambda l: l.product_id == rec).mapped('over_shot')),3),\
                } for rec in balance_ids.balance_rep_pro_session_ids.mapped('product_id') if balance_ids.balance_rep_pro_session_ids]

        user = self.env['res.users'].browse(data.get('context').get('uid'))
        currency_id = balance_ids[0].company_id.currency_id if balance_ids else False
        return {
            'start_date': data.get('start_date'),
            'end_date': data.get('end_date'),
            'docs': balance_ids,
            'user': user,
            'currency_id': currency_id,
            'nozzle_data': nozzle_bifercate_id,
            'total_product_sales': total_product_sales,
            'nozzle_reading_by_pos_session': nozzle_reading_by_pos_session,
        }
