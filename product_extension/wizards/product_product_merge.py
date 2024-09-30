# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.exceptions import ValidationError

from odoo import fields, api, models, _


class ProductProductMerge(models.TransientModel):
    _name = "product.product.merge.details"
    _description = "Product Product Merge"
    _order = "sequence,id"

    product_id = fields.Many2one('product.product', string='Product template merge')
    is_mail_product_template = fields.Boolean(related='product_id.is_merged_product', string="Main Product")
    product_merge_id = fields.Many2one('product.product.merge', string='Product merge Record')
    is_main_product = fields.Boolean(string="Main Product", related='product_id.is_main_product')
    attribute_id = fields.Many2many(
        comodel_name='product.attribute',
        string="Attribute",
        index=True)
    sequence = fields.Integer("Record Sequence")

    value_attr_ids = fields.Many2many('product.attribute.value', 'rel_product_product_attribute_value',
                                      'product_id', 'attribute_id',
                                      string="Values",
                                      domain="[('attribute_id', 'in', attribute_id)]")

    @api.onchange('value_attr_ids')
    def onchange_check_attribute_values(self):
        for self in self:
            for attribute in self.attribute_id._origin:

                attribute_value_ids = self.value_attr_ids._origin
                attribute_values = attribute_value_ids.filtered(lambda x: x.attribute_id.id == attribute.id)
                if len(attribute_values) > 1:
                    raise ValidationError('You cannot select multiple value from perticular category.')


class ProductProductMergeWizard(models.TransientModel):
    _name = "product.product.merge"
    _description = "Product Template Merge"

    product_merge_id = fields.One2many('product.product.merge.details', 'product_merge_id',
                                       string='Product template merge List')

    process_type = fields.Selection([
        ('merge_product', 'Merge Product'),
        ('change_attribute', 'Change Attribute'),
    ], string="Process Type")

    def merge_product_product_data(self):
        merge_product_list = self.product_merge_id

        main_product_ids = merge_product_list.mapped('product_id').filtered(
            lambda x: x.is_main_product)
        if main_product_ids:
            main_product_id = main_product_ids[0]
        else:
            main_product_id = merge_product_list[0].product_id
            main_product_id.write({
                'is_main_product': True
            })

        main_product_template_id = main_product_id.product_tmpl_id

        attribute_id_dict = {}
        remaining_product_template_list = merge_product_list.mapped('product_id').product_tmpl_id

        # Preparing Attribute and attribute value list
        for merge_product in merge_product_list:
            attributes_id = merge_product.attribute_id
            for attribute_id in attributes_id:
                value_attr_ids = merge_product.value_attr_ids.filtered(lambda x: x.attribute_id == attribute_id)
                if value_attr_ids:
                    for value_attr_id in value_attr_ids:
                        if attribute_id.id in attribute_id_dict:
                            attribute_id_dict[attribute_id.id].append(value_attr_id.id)
                        else:
                            attribute_id_dict[attribute_id.id] = [value_attr_id.id]

        # Updating or adding Attribute and attribute value in main Product
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
                main_product_template_id.with_context({
                    'from_merge_product': True,
                    'merge_record': self.id,
                }).write({
                    'attribute_line_ids': product_template_attribute_line,
                    'is_merged_product': True
                })
        else:
            product_template_attribute_line = []
            for attribute_id in attribute_id_dict:
                product_template_attribute_line.append([0, 0, {
                    'attribute_id': attribute_id,
                    'value_ids': list(set(attribute_id_dict[attribute_id]))
                }])

            main_product_template_id.with_context({
                'from_merge_product': True,
                'merge_record': self.id,
            }).write({
                'attribute_line_ids': product_template_attribute_line,
                'is_merged_product': True
            })

        # Adding attributes to product.
        for merge_product in merge_product_list:
            attribute_values_list = merge_product.value_attr_ids.ids
            product_template_attribute_ids = self.env['product.template.attribute.value'].search([
                ('product_tmpl_id', '=', main_product_template_id.id),
                ('product_attribute_value_id', 'in', attribute_values_list)
            ])

            if product_template_attribute_ids:
                merge_product_dict = {
                    'product_tmpl_id': main_product_template_id.id,
                    'product_template_attribute_value_ids': [(6, 0, product_template_attribute_ids.ids)],
                }
                if merge_product.value_attr_ids:
                    merge_product_dict['value_attr_ids'] = [(6, 0, merge_product.value_attr_ids.ids)]

                merge_product.product_id.write(merge_product_dict)
                self.env.flush_all()
                self.env.invalidate_all()

        # Archieving remaining template
        remaining_product_template_ids = remaining_product_template_list.filtered(
            lambda x: x.id != main_product_template_id.id
        )

        if remaining_product_template_ids:
            remaining_product_template_ids.write({
                'active': False
            })

        # returning action for main product view.
        return {
            'name': _('Products'),
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'form',
            'view_id': self.env.ref('product.product_template_only_form_view').sudo().id,
            'res_id': main_product_template_id.id,
            'target': 'current',
        }

    def change_attribute_product_record(self):
        product_merge_ids = self.product_merge_id
        for product_merge_id in product_merge_ids:
            product_template_id = product_merge_id.product_id.product_tmpl_id
            product_template_id_old_attribute_ids = product_merge_id.product_id.product_template_attribute_value_ids
            # Preparing Attribute and attribute value list
            attribute_id_dict = {}
            attributes_id = product_merge_id.attribute_id
            for attribute_id in attributes_id:
                value_attr_ids = product_merge_id.value_attr_ids.filtered(lambda x: x.attribute_id == attribute_id)
                if value_attr_ids:
                    for value_attr_id in value_attr_ids:
                        if attribute_id.id in attribute_id_dict:
                            attribute_id_dict[attribute_id.id].append(value_attr_id.id)
                        else:
                            attribute_id_dict[attribute_id.id] = [value_attr_id.id]
            # Updating or adding Attribute and attribute value in main Product
            if product_template_id.attribute_line_ids:
                product_template_attribute_line = []
                for attribute_id in attribute_id_dict:
                    attribute_id_record = product_template_id.attribute_line_ids.filtered(
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
                    product_template_id.with_context({
                        'from_merge_product': True,
                        'merge_record': self.id,
                    }).write({
                        'attribute_line_ids': product_template_attribute_line,
                        'is_merged_product': True
                    })
            else:
                product_template_attribute_line = []
                for attribute_id in attribute_id_dict:
                    product_template_attribute_line.append([0, 0, {
                        'attribute_id': attribute_id,
                        'value_ids': list(set(attribute_id_dict[attribute_id]))
                    }])

                product_template_id.with_context({
                    'from_merge_product': True,
                    'merge_record': self.id,
                }).write({
                    'attribute_line_ids': product_template_attribute_line,
                    'is_merged_product': True
                })

            # Adding attributes to product.
            attribute_values_list = product_merge_id.value_attr_ids.ids
            product_template_attribute_ids = self.env['product.template.attribute.value'].search([
                ('product_tmpl_id', '=', product_template_id.id),
                ('product_attribute_value_id', 'in', attribute_values_list)
            ])
            if product_template_attribute_ids:
                merge_product_dict = {
                    'product_template_attribute_value_ids': [(6, 0, product_template_attribute_ids.ids)],
                }
                if product_merge_id.value_attr_ids:
                    merge_product_dict['value_attr_ids'] = [(6, 0, product_merge_id.value_attr_ids.ids)]

                product_merge_id.product_id.write(merge_product_dict)
                self.env.flush_all()
                self.env.invalidate_all()

            # remaining attribute remove
            merge_product_attribute_id_dict = {}
            remove_product_attribute_old_template = []
            remaining_product_attribute_ids = product_template_id_old_attribute_ids.filtered(
                lambda x: x.id not in product_template_attribute_ids.ids)
            if remaining_product_attribute_ids:
                for attribute in remaining_product_attribute_ids:
                    if attribute.attribute_id.id in merge_product_attribute_id_dict:
                        merge_product_attribute_id_dict[attribute.attribute_id.id].append(
                            attribute.product_attribute_value_id.id)
                    else:
                        merge_product_attribute_id_dict[attribute.attribute_id.id] = [
                            attribute.product_attribute_value_id.id]

                for product_attribute_id in merge_product_attribute_id_dict:
                    attribute_id_record = product_template_id.attribute_line_ids.filtered(
                        lambda x: x.attribute_id.id == product_attribute_id
                    )
                    if len(attribute_id_record.value_ids.ids) == len(
                            merge_product_attribute_id_dict[product_attribute_id]):
                        remove_product_attribute_old_template.append([2, attribute_id_record.id])
                    else:
                        value_ids_pass_value = [[3, attribute] for attribute in
                                                merge_product_attribute_id_dict[product_attribute_id]]

                        remove_product_attribute_old_template.append([
                            1, attribute_id_record.id, {
                                'value_ids': value_ids_pass_value
                            }])
                if remove_product_attribute_old_template:
                    product_template_id.with_context({
                        'from_merge_product': True,
                    }).write({
                        'attribute_line_ids': remove_product_attribute_old_template
                    })

    def merge_product_product_list(self):

        if self.process_type and self.process_type == 'merge_product':
            data = self.merge_product_product_data()
            return data
        elif self.process_type and self.process_type == 'change_attribute':
            self.change_attribute_product_record()
        else:
            raise ValidationError('Please choose type of process which you want to perform.')

    def update_product_attributes(self):
        attribute_list = self.product_merge_id[0].attribute_id.ids
        if attribute_list:
            for product in self.product_merge_id:
                product.write({
                    'attribute_id': [(6, 0, attribute_list)]
                })
        return {
            'res_model': 'product.product.merge',
            'view_mode': 'form',
            'name': "Merge Product product",
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
        }
