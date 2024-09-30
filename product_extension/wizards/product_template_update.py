# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplateUpdateWizard(models.TransientModel):
    _name = "product.template.update"
    _description = "Product Template Update"

    product_tmpl_id = fields.Many2one('product.template', string='Product', default=False)

    def update_product_template_from_product(self):
        product_ids = self.env.context.get('product_ids')
        if product_ids:
            product_ids_obj = self.env['product.product'].browse(product_ids)
            old_product_tmpl_id = product_ids_obj[0].product_tmpl_id
            new_product_tmpl_id = self.product_tmpl_id
            attribute_ids = product_ids_obj.mapped('product_template_attribute_value_ids')

            # preparing dictionary for Unlink attribute from Product template
            remaining_product_ids = old_product_tmpl_id.mapped('product_variant_ids').filtered(
                lambda x: x.id not in product_ids)
            if remaining_product_ids:
                remaining_product_attributes = remaining_product_ids.mapped('product_template_attribute_value_ids')
                merge_product_attributes = attribute_ids.filtered(
                    lambda x: x.id not in remaining_product_attributes.ids)
            else:
                merge_product_attributes = attribute_ids

            merge_product_attribute_id_dict = {}
            remove_product_attribute_old_template = []
            for attribute in merge_product_attributes:
                if attribute.attribute_id.id in merge_product_attribute_id_dict:
                    merge_product_attribute_id_dict[attribute.attribute_id.id].append(
                        attribute.product_attribute_value_id.id)
                else:
                    merge_product_attribute_id_dict[attribute.attribute_id.id] = [
                        attribute.product_attribute_value_id.id]

            for product_attribute_id in merge_product_attribute_id_dict:
                attribute_id_record = old_product_tmpl_id.attribute_line_ids.filtered(
                    lambda x: x.attribute_id.id == product_attribute_id
                )
                if len(attribute_id_record.value_ids.ids) == len(merge_product_attribute_id_dict[product_attribute_id]):
                    remove_product_attribute_old_template.append([2, attribute_id_record.id])
                else:
                    value_ids_pass_value = [[3, attribute] for attribute in
                                            merge_product_attribute_id_dict[product_attribute_id]]

                    remove_product_attribute_old_template.append([
                        1, attribute_id_record.id, {
                            'value_ids': value_ids_pass_value
                        }])

            # prepare attribute list for new product.
            new_template_attribute_dict = {}

            for attribute in attribute_ids:
                if attribute.attribute_id.id in new_template_attribute_dict:
                    new_template_attribute_dict[attribute.attribute_id.id].append(
                        attribute.product_attribute_value_id.id)
                else:
                    new_template_attribute_dict[attribute.attribute_id.id] = [
                        attribute.product_attribute_value_id.id]

            # Updating or adding Attribute and attribute value in main Product
            if new_product_tmpl_id.attribute_line_ids:
                product_template_attribute_line = []
                for attribute_id in new_template_attribute_dict:
                    attribute_id_record = new_product_tmpl_id.attribute_line_ids.filtered(
                        lambda x: x.attribute_id.id == attribute_id
                    )
                    if attribute_id_record:
                        for value in new_template_attribute_dict[attribute_id]:
                            if value in attribute_id_record.value_ids.ids:
                                continue
                            else:
                                attribute_id_record.with_context({
                                    'from_merge_product': True,
                                }).write({
                                    'value_ids': [(4, value)]
                                })
                    else:
                        product_template_attribute_line.append([0, 0, {
                            'attribute_id': attribute_id,
                            'value_ids': list(set(new_template_attribute_dict[attribute_id]))
                        }])
                if product_template_attribute_line:
                    new_product_tmpl_id.with_context({
                        'from_merge_product': True,
                    }).write({
                        'attribute_line_ids': product_template_attribute_line,
                        'is_merged_product': True
                    })
            else:
                product_template_attribute_line = []
                for attribute_id in new_template_attribute_dict:
                    product_template_attribute_line.append([0, 0, {
                        'attribute_id': attribute_id,
                        'value_ids': list(set(new_template_attribute_dict[attribute_id]))
                    }])

                new_product_tmpl_id.with_context({
                    'from_merge_product': True,
                }).write({
                    'attribute_line_ids': product_template_attribute_line,
                    'is_merged_product': True
                })

            # Adding attributes to product.
            for product_id in product_ids_obj:
                attribute_values_list = product_id.product_template_attribute_value_ids.mapped(
                    'product_attribute_value_id').ids
                product_template_attribute_ids = self.env['product.template.attribute.value'].search([
                    ('product_tmpl_id', '=', new_product_tmpl_id.id),
                    ('product_attribute_value_id', 'in', attribute_values_list)
                ])
                if product_template_attribute_ids:
                    self.env.flush_all()
                    if ((len(new_product_tmpl_id.product_variant_ids) == 1) and
                            (
                                    new_product_tmpl_id.product_variant_ids.product_template_attribute_value_ids.ids == product_template_attribute_ids.ids)):
                        unlink_attribute_ids = [[3, attribute] for attribute in
                                                new_product_tmpl_id.product_variant_ids.product_template_attribute_value_ids.ids]

                        new_product_tmpl_id.product_variant_ids.write({
                            'product_template_attribute_value_ids': unlink_attribute_ids
                        })
                        self.env.flush_all()
                        self.env.invalidate_all()

                    product_id.write({
                        'product_tmpl_id': new_product_tmpl_id.id,
                        'product_template_attribute_value_ids': [(6, 0, product_template_attribute_ids.ids)]
                    })
                    self.env.flush_all()
                    self.env.invalidate_all()

            old_product_tmpl_id.with_context({
                'from_merge_product': True,
            }).write({
                'attribute_line_ids': remove_product_attribute_old_template
            })
