# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import ValidationError

from odoo import fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    attribute_id = fields.Many2many(
        comodel_name='product.attribute',
        string="Attribute",
        index=True)

    value_attr_ids = fields.Many2many('product.attribute.value', 'rel_product_product_attribute_value_detail',
                                      'product_id', 'attribute_id',
                                      string="Values")

    is_main_product = fields.Boolean(string="Main Product")
    
    product_template_variant_value_ids = fields.Many2many('product.template.attribute.value', relation='product_variant_combination',
                                                         string="Variant Values", ondelete='restrict', domain=[])
    
    barcode_label_description = fields.Char("Barcode Label Description")

    def get_product_product_merge_view(self):
        product_list = []
        if self:
            main_product = self.filtered(lambda X: X.is_main_product == True)
            if main_product:
                for main_product in main_product:
                    product_list.append([0, 0, {
                        'product_id': main_product.id,
                        'attribute_id': [(6, 0, main_product.value_attr_ids.mapped('attribute_id').ids)],
                        'value_attr_ids': [(6, 0, main_product.value_attr_ids.ids)]
                    }
                                         ])
            for product in self:
                if product.id not in main_product.ids:
                    product_list.append([0, 0, {
                        'product_id': product.id,
                        'attribute_id': [(6, 0, product.value_attr_ids.mapped('attribute_id').ids)],
                        'value_attr_ids': [(6, 0, product.value_attr_ids.ids)]
                    }])
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'product.product.merge',
                'view_type': 'form',
                'view_mode': 'form',
                'name': _('Merge Product Product'),
                'target': 'new',
                'context': {
                    'default_product_merge_id': product_list,
                },
            }
        else:
            raise ValidationError('Please select product.')

    def get_product_template_update_view(self):
        if self:
            product_ids = self.filtered(lambda x: x.product_template_attribute_value_ids)
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'product.template.update',
                'view_type': 'form',
                'view_mode': 'form',
                'name': _('Update Product Template'),
                'target': 'new',
                'context': {
                    'product_ids': product_ids.ids,
                },
            }
        else:
            raise ValidationError('Please select product.')
