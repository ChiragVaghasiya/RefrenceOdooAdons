# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.exceptions import ValidationError

from odoo import fields, api, models


class ProductMerge(models.TransientModel):
    _name = "product.template.merge.details"
    _description = "Product Template Merge"
    _order = "sequence,id"

    product_tmpl_id = fields.Many2one('product.template', string='Product template merge')
    is_mail_product_template = fields.Boolean(related='product_tmpl_id.is_merged_product', string="Main Product")
    product_merge_id = fields.Many2one('product.template.merge', string='Product merge Record')

    attribute_id = fields.Many2many(
        comodel_name='product.attribute',
        string="Attribute",
        index=True)
    sequence = fields.Integer("Record Sequence")

    value_attr_ids = fields.Many2many('product.attribute.value', 'rel_product_template_attribute_value',
                                      'product_tmpl_id', 'attribute_id',
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


class ProductMergeWizard(models.TransientModel):
    _name = "product.template.merge"
    _description = "Product Template Merge"

    product_tmpl_merge_id = fields.One2many('product.template.merge.details', 'product_merge_id',
                                            string='Product template merge List')

    def merge_product_template_list(self):
        merge_product_list = self.product_tmpl_merge_id
        main_product_template_ids = merge_product_list.mapped('product_tmpl_id').filtered(
            lambda x: x.is_merged_product)
        if main_product_template_ids:
            main_product_template_id = main_product_template_ids[0]
        else:
            main_product_template_id = merge_product_list[0].product_tmpl_id

        attribute_id_dict = {}

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
                merge_product.product_tmpl_id.product_variant_id.write({
                    'product_tmpl_id': main_product_template_id.id,
                    'product_template_attribute_value_ids': [(6, 0, product_template_attribute_ids.ids)]
                })
                self.env.flush_all()
                self.env.invalidate_all()

        # Archieving remaining template
        remaining_product_template_list = merge_product_list.mapped('product_tmpl_id').filtered(
            lambda x: x.id != main_product_template_id.id
        )
        if remaining_product_template_list:
            remaining_product_template_list.write({
                'active': False
            })
