from odoo import models, fields, api,_
import io
import os
import base64
from odoo.exceptions import ValidationError
import pandas as pd
import logging
_logger = logging.getLogger(__name__)

class ValidationErrorRecords(models.TransientModel):
    _name = 'validation.error.records'
    _description = "Validation Error Records"
    
    custom_update_id = fields.Many2one('custom.update.product',string="Custom Product Update") 
    name = fields.Text("Validation Error")
    sheet_row = fields.Char("Sheet Row")
    record_id = fields.Char("Product ID")
    product_name = fields.Char("Product Name")
    

class CustomImportModel(models.TransientModel):
    _name = 'custom.update.product'
    _description = "Custom Update Product"

    data_file = fields.Binary(string="File", required=True)
    file_name = fields.Char(string="File name")
    flag_row = fields.Integer(string="Updated Record",default=0)
    total_record = fields.Integer(string="Total record",default=0)
    validation_error_ids = fields.One2many('validation.error.records','custom_update_id',string="Validation error Records",)
    
    process_type = fields.Selection([
        ('merge_product', 'Merge & update Product'),
        ('update_product', 'Update product')
    ], string="Process Type", required=True)
    
    def _read_excel(self, file_data):
        # Decode the file
        file_content = base64.b64decode(file_data)
        # Read the Excel file
        data = pd.read_excel(io.BytesIO(file_content))
        return data

    @api.onchange('data_file')
    def onchange_calculate_total_record(self):
        if self.data_file:
            data = self._read_excel(self.data_file)
            if self.process_type == 'merge_product':     
                rows = data.to_dict(orient='records')
                # last_template_id = rows[-1].get('Template ID')
                # self.total_record = last_template_id
                template_id = 0
                flag_template_id_name = ''
                #Find Total Template no.
                for row_index,row in enumerate(rows):
                    for col_index,(header,vals) in enumerate(row.items()):
                        vals = vals.strip() if isinstance(vals,str) else vals
                        if header == 'Template Name':
                            if not vals or pd.isnull(vals):
                                break
                        else:
                            continue 
                        template_id_name = vals
                        if template_id_name != flag_template_id_name:
                            flag_template_id_name = template_id_name 
                            template_id += 1
                total_records = template_id
                self.total_record = total_records
            else:    
                self.total_record = len(data)
        else:
            self.total_record = 0
    
    def update_product_product_records(self):
        if self.data_file:
            data = self._read_excel(self.data_file)
            rows = data.to_dict(orient='records')
            
            if self.process_type == 'merge_product':
                template_id = 0
                flag_template_id_name = ''
                #Find Total Template no.
                for row_index,row in enumerate(rows):
                    for col_index,(header,vals) in enumerate(row.items()):
                        vals = vals.strip() if isinstance(vals,str) else vals
                        if header == 'Template Name':
                            if not vals or pd.isnull(vals):
                                break
                        else:
                            continue 
                        template_id_name = vals
                        if template_id_name != flag_template_id_name:
                            flag_template_id_name = template_id_name 
                            template_id += 1
                total_records = template_id
                self.total_record = total_records    
            else:
                total_records = len(data)
                self.total_record = total_records
             
            updated_record = self.with_context(Test = True).update_product_details(rows,self.flag_row,total_records)
            self.flag_row = updated_record

            if updated_record < total_records:
                # return updated_record
                self.env.cr.commit()
                re_update = self.update_product_product_records()
                return re_update
                # return {
                #     'type': 'ir.actions.act_window',
                #     'res_model': 'custom.update.product',
                #     'name':"Update Product",
                #     'view_mode': 'form',
                #     'view_type': 'form',
                #     'res_id': self.id,
                #     'views': [(False, 'form')],
                #     'target': 'new',
                #     'view_id': self.env.ref('product_extension.view_custom_import_model_form').sudo().id,
                # }
            else:
                if self.validation_error_ids:
                    return {
                        'type': 'ir.actions.act_window',
                        'res_model': 'custom.update.product',
                        'name':"Update Product",
                        'view_mode': 'form',
                        'view_type': 'form',
                        'res_id': self.id,
                        'views': [(False, 'form')],
                        'target': 'new',
                        'view_id': self.env.ref('product_extension.view_custom_import_model_form').sudo().id,
                    }
                else:    
                    return {
                        'effect': {
                            'type': 'rainbow_man',
                            'message': _("Product updated successfully"),
                        }
                    }
        else:
            raise ValidationError("Please Upload File")  
        
    
    def update_product_details(self,rows,flag_row = 0,total_record = 0):
        flag_template_id_name = ''
        template_id = 0
        template_id_updated = flag_row
        #main product id
        flag_main_product_external_id = None
        main_product_template_name = ''
        
        
        if self.process_type == 'update_product':
            limit_row = (flag_row + 500) if (flag_row + 500) <= total_record else total_record
            start_point = flag_row
        else:
            limit_row = (flag_row + 50) if (flag_row + 50) <= total_record else total_record
            start_point = flag_row
            
        extend_flag = 0
        for row_index,row in enumerate(rows):
            
            if self.process_type == 'update_product':
                if (row_index > limit_row) or (row_index < start_point):
                    continue
                extend_flag += 1
                
            print("row_index == ",row_index)
            _logger.info('row_index ==  %s',row_index)
            #preparning Attribute Dictionary
            attribute_id_dict = {}
            value_ids_list = []
            
            #current Product Id
            flag_product_external_id = None
            test_flag = 0
            product_update_dict = {}
            attribute_col_index = 1000
            
            try:
                product_template_break = 0
                for col_index,(header,vals) in enumerate(row.items()):
                    
                    vals = vals.strip() if isinstance(vals,str) else vals
                    #Finding Column for Attributes
                    if header.startswith("x_") and header == 'x_At':
                        attribute_col_index = col_index 
                                                                            
                    if header == 'ID':
                        flag_product_external_id = vals
                    
                    # #Adjust Main product for product merge
                    # if header == 'Template ID':
                    #     if self.process_type == 'merge_product':
                    #         template_id = vals
                    #         if (template_id > limit_row) or (template_id <= start_point):
                    #             product_template_break = 1
                    #             break
                    #         if template_id != flag_template_id:
                    #             flag_template_id = template_id
                    #             test_flag = 1
                    #         else:
                    #             test_flag = 0
                    #     continue
                    
                    #Adjust Main product for product merge
                    if header == 'Template Name':
                        if self.process_type == 'merge_product':    
                            if not vals or pd.isnull(vals):
                                product_template_break = 1
                                break
                            template_id_name = vals
                            if template_id_name != flag_template_id_name:
                                flag_template_id_name = template_id_name
                                test_flag = 1
                                main_product_template_name = vals
                                flag_main_product_external_id = flag_product_external_id
                                template_id += 1
                            else:
                                test_flag = 0
                            
                            update_test_flag = 0
                            if (template_id > limit_row) or (template_id <= start_point):
                                product_template_break = 1
                                break
                            else:
                                update_test_flag = 1
                                
                            if test_flag and update_test_flag:
                                template_id_updated += 1           
                        continue
                        
                        
                    if not vals or pd.isnull(vals):
                        continue   
                    
                    if not flag_product_external_id:
                        break
                    product_id = self.env['product.product'].sudo().browse(int(flag_product_external_id))
                    
                    # if header == 'Template Name' and test_flag == 1:
                    #     main_product_template_name = vals  
        
                    if header == 'Can be Sold':
                        product_update_dict['sale_ok'] = vals
                        continue
                    if header == 'Can be Purchased':
                        product_update_dict['purchase_ok'] = vals
                        continue
                    
                    # if header == 'Product Type':
                    #     if product_id.detailed_type != vals:
                    #         product_update_dict['detailed_type'] = vals
                    #     continue 
                    
                    if header == 'Product Name':
                        if product_id.name != vals:
                            if self.process_type == 'update_product':
                                product_update_dict['name'] = vals
                        
                        
                    if header == 'Invoicing Policy':
                        if product_id.invoice_policy != vals:
                            product_update_dict['invoice_policy'] = vals
                        continue
                    
                    # if header == 'Unit of Measure':
                    #     if product_id.uom_id.name != vals:
                    #         measure_id = self.env['uom.uom'].search([('name','=',vals)])
                    #         if measure_id:
                    #             product_update_dict['uom_id'] = measure_id.id
                    #     continue
                    
                    # if header == 'Purchase UoM':
                    #     if product_id.uom_po_id.name != vals:
                    #         measure_id = self.env['uom.uom'].search([('name','=',vals)])
                    #         if measure_id:
                    #             product_update_dict['uom_po_id'] = measure_id.id
                    #     continue
                            
                    if header == 'Sales Price':
                        if product_id.lst_price != vals:
                            product_update_dict['lst_price'] = vals
                            
                    if header == 'Cost':
                        if product_id.standard_price != vals:
                            product_update_dict['standard_price'] = vals        
                    
                    if header == 'Internal Reference':
                        if product_id.default_code != vals:
                            product_update_dict['default_code'] = vals
                            
                    if header == 'Barcode':
                        if isinstance(vals, float):
                            vals = int(vals)
                        if product_id.barcode != vals:
                            product_update_dict['barcode'] = vals
                            
                    if header == 'BARCODE LABEL DISCRIPTION':
                        if product_id.barcode_label_description != vals:
                            product_update_dict['barcode_label_description'] = vals
                              
                    if header == 'Company':
                        if product_id.company_id.name != vals:
                            company_id = self.env['res.company'].search([('name','=',vals)])
                            if company_id:
                                product_update_dict['company_id'] = company_id.id          
                            
                    if header == 'INTERNAL NOTES':
                        if product_id.description != vals:
                            product_update_dict['description'] = vals
                    
                    if header == 'Website':
                        if product_id.website_id.name != vals:
                            website_id = self.env['website'].search([('name','=',vals)])
                            if website_id:
                                product_update_dict['website_id'] = website_id.id
                                
                    if header == 'Website Sequence':
                        if product_id.website_sequence != vals:
                            product_update_dict['website_sequence'] = vals
                            
                    if header == 'Out-of-Stock':
                        if product_id.allow_out_of_stock_order != vals:
                            product_update_dict['allow_out_of_stock_order'] = vals
                    
                    if header == 'Show Available Qty':
                        if product_id.show_availability != vals:
                            product_update_dict['show_availability'] = vals
                    
                    if header == 'Out-of-Stock Message':
                        if product_id.out_of_stock_message != vals:
                            product_update_dict['out_of_stock_message'] = vals
                                
                    if header == 'SALES DESCRIPTION':
                        if product_id.description_sale != vals:
                            product_update_dict['description_sale'] = vals
                    
                    if header == 'WARNING WHEN SELLING THIS PRODUCT':
                        if product_id.sale_line_warn != vals:
                            product_update_dict['sale_line_warn'] = vals
                    
                    if header == 'Control Policy':
                        if product_id.purchase_method != vals:
                            product_update_dict['purchase_method'] = vals
                    
                    if header == 'PURCHASE DESCRIPTION':
                        if product_id.description_purchase != vals:
                            product_update_dict['description_purchase'] = vals
                    
                    if header == 'WARNING WHEN PURCHASING THIS PRODUCT':
                        if product_id.purchase_line_warn != vals:
                            product_update_dict['purchase_line_warn'] = vals
                    
                    if header == 'Tracking':
                        if product_id.tracking != vals:
                            product_update_dict['tracking'] = vals  
                    
                    if header == 'Weight':
                        if product_id.weight != vals:
                            product_update_dict['weight'] = vals  
                    
                    if header == 'Volume':
                        if product_id.volume != vals:
                            product_update_dict['volume'] = vals  
                    
                    if header == 'Customer Lead Time':
                        if product_id.sale_delay != vals:
                            product_update_dict['sale_delay'] = vals  
                    
                    if header == 'HS Code':
                        if product_id.hs_code != vals:
                            product_update_dict['hs_code'] = vals  
                    
                    if header == 'Origin of Goods':
                        if product_id.country_of_origin.name != vals:
                            country_of_origin = self.env['res.country'].search([('name','=',vals)])
                            if country_of_origin:
                                product_update_dict['country_of_origin'] = country_of_origin.id  
                                                                                    
                    #update column which name start with 'X_'
                    if header.startswith("x_") and header != 'x_At':
                        if product_id[header] != vals:
                            product_update_dict[header] = vals
                                                                                                                                                                                                        
                    # Generate Attribute and Value IF not available and Prepare dictionary to add in product.
                    if col_index > attribute_col_index:
                        attribute_id = self.env['product.attribute'].search([('name','=',header.strip())])
                        if attribute_id: 
                            attr_value_id = self.env['product.attribute.value'].search([('attribute_id','=',attribute_id.id),('name','=',str(vals))])
                            if not vals or pd.isnull(vals):
                                continue
                            if not attr_value_id:
                                print(vals,attribute_id.name)
                                attr_value_id = self.env['product.attribute.value'].sudo().create({
                                    'name':vals,
                                    'attribute_id':attribute_id.id
                                })
                                
                            if attribute_id.id in attribute_id_dict:
                                attribute_id_dict[attribute_id.id].append(attr_value_id.id)
                                value_ids_list.append(attr_value_id.id)
                            else:
                                attribute_id_dict[attribute_id.id] = [attr_value_id.id]
                                value_ids_list.append(attr_value_id.id)      
                        else:
                            attr_dict = {
                                'name':header.strip(),
                                'create_variant':'dynamic'
                            }
                            if not vals or pd.isnull(vals):
                                attribute_id = self.env['product.attribute'].sudo().create(attr_dict)
                                continue
                            else:
                                attr_dict['value_ids'] = [(0,0,{
                                    'name':vals
                                })]
                            
                            attribute_id = self.env['product.attribute'].sudo().create(attr_dict)
                            
                            attr_value_id = self.env['product.attribute.value'].sudo().search([('attribute_id','=',attribute_id.id),('name','=',vals)])
                            
                            if attribute_id.id in attribute_id_dict:
                                attribute_id_dict[attribute_id.id].append(attr_value_id.id)
                                value_ids_list.append(attr_value_id.id)
                            else:
                                attribute_id_dict[attribute_id.id] = [attr_value_id.id]
                                value_ids_list.append(attr_value_id.id)
                                            
                    col_index +=1
                
                if product_template_break == 1:
                    continue
                
                if not flag_product_external_id:
                    continue
                
                product_id = self.env['product.product'].sudo().browse(int(flag_product_external_id))
                
                product_id.write(product_update_dict)
                
                main_product_id = self.env['product.product'].sudo().browse(int(flag_main_product_external_id) if flag_main_product_external_id else None)
                if self.process_type == 'update_product':
                    main_product_template_id  = product_id.product_tmpl_id
                else:  
                    main_product_template_id  = main_product_id.product_tmpl_id
                old_product_template_id = product_id.product_tmpl_id
                
                update_product_template = {}
                #Update Product Template Name for Main template
                
                _logger.info('main_product_template_id ==  %s',main_product_template_id)
                _logger.info('old_product_template_id ==  %s',old_product_template_id)
                if main_product_template_id.attribute_line_ids:
                    product_template_attribute_line = []
                    for attribute_id in attribute_id_dict:
                        attribute_id_record = main_product_template_id.attribute_line_ids.filtered(
                            lambda x: x.attribute_id.id == attribute_id
                        )
                        if attribute_id_record:
                            for value in attribute_id_dict[attribute_id]:
                                if value in attribute_id_record.value_ids.ids:
                                    continue
                                else:
                                    attribute_id_record.with_context({
                                        'from_merge_product': True,
                                        'merge_record': self.id,
                                    }).write({
                                        'value_ids': [(4, value)]
                                    })
                        else:
                            product_template_attribute_line.append([0, 0, {
                                'attribute_id': attribute_id,
                                'value_ids': list(set(attribute_id_dict[attribute_id]))
                            }])
                    if product_template_attribute_line:
                        update_product_template.update({
                            'attribute_line_ids': product_template_attribute_line,
                            'is_merged_product': True
                        })
                    
                        main_product_template_id.with_context({
                            'from_merge_product': True,
                            'merge_record': self.id,
                        }).write(update_product_template)
                else:
                    product_template_attribute_line = []
                    for attribute_id in attribute_id_dict:
                        product_template_attribute_line.append([0, 0, {
                            'attribute_id': attribute_id,
                            'value_ids': list(set(attribute_id_dict[attribute_id]))
                        }])
                    update_product_template.update({
                            'attribute_line_ids': product_template_attribute_line,
                            'is_merged_product': True
                        })   
                    main_product_template_id.with_context({
                        'from_merge_product': True,
                        'merge_record': self.id,
                    }).write(update_product_template)
                    
                
                # Adding attributes to product.
                attribute_values_list = value_ids_list
                product_template_attribute_ids = self.env['product.template.attribute.value'].search([
                    ('product_tmpl_id', '=', main_product_template_id.id),
                    ('product_attribute_value_id', 'in', attribute_values_list)
                ])
                
                if product_template_attribute_ids:
                    merge_product_dict = {
                        'product_tmpl_id': main_product_template_id.id,
                        'product_template_attribute_value_ids': [(6, 0, product_template_attribute_ids.ids)],
                    }
                    product_id.write(merge_product_dict)
                    self.env.cr.commit()
                    self.env.flush_all()
                    self.env.invalidate_all()
                
                if main_product_template_id.id != old_product_template_id.id and len(old_product_template_id.product_variant_ids) <= 1:
                    old_product_template_id.write({
                        'active': False
                    })
                
                if test_flag == 1 and self.process_type == 'merge_product' and main_product_template_name:
                    main_product_template_id.write({
                        'name':main_product_template_name
                    })
                
                row_index += 1
            except Exception as e:
                self.env.cr.rollback()
                self.env['validation.error.records'].create({
                    'name':e,
                    'record_id':flag_product_external_id,
                    'sheet_row':row_index + 2,
                    'custom_update_id':self.id,
                    'product_name':product_id.name
                })
                self.env.cr.commit()
                continue
         
        if self.process_type == 'update_product':
            if start_point == 0:
                updated_record = extend_flag
            else:
                updated_record = extend_flag + start_point
        else:
            updated_record = template_id_updated 
             
        return updated_record
    