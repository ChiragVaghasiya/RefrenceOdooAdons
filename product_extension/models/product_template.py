# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import itertools

from odoo.exceptions import UserError, ValidationError

from odoo import fields, models, _, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_merged_product = fields.Boolean(string="Is Megred Product")

    @api.model
    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        return result

    def get_product_merge_view(self):
        product_template_list = []
        if self:
            merged_product_template = self.filtered(lambda X: X.is_merged_product == True)
            if merged_product_template:
                for merged_product in merged_product_template:
                    product_template_list.append([0, 0, {
                        'product_tmpl_id': merged_product.id
                    }
                                                  ])
            for product_template in self:
                if product_template.id not in merged_product_template.ids:
                    product_template_list.append([0, 0, {
                        'product_tmpl_id': product_template.id
                    }
                                                  ])
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'product.template.merge',
                'view_type': 'form',
                'view_mode': 'form',
                'name': _('Merge Product Template'),
                'target': 'new',
                'context': {
                    'default_product_tmpl_merge_id': product_template_list,
                },
            }
        else:
            raise ValidationError('Please select product template.')

    def _create_variant_ids(self):
        if not self:
            return
        self.env.flush_all()
        Product = self.env["product.product"]

        variants_to_create = []
        variants_to_activate = Product
        variants_to_unlink = Product

        for tmpl_id in self:
            lines_without_no_variants = tmpl_id.valid_product_template_attribute_line_ids._without_no_variant_attributes()

            all_variants = tmpl_id.with_context(active_test=False).product_variant_ids.sorted(
                lambda p: (p.active, -p.id))

            current_variants_to_create = []
            current_variants_to_activate = Product

            # adding an attribute with only one value should not recreate product
            # write this attribute on every product to make sure we don't lose them
            single_value_lines = lines_without_no_variants.filtered(
                lambda ptal: len(ptal.product_template_value_ids._only_active()) == 1)
            if single_value_lines:
                for variant in all_variants:
                    combination = variant.product_template_attribute_value_ids | single_value_lines.product_template_value_ids._only_active()
                    # Do not add single value if the resulting combination would
                    # be invalid anyway.
                    if (
                            len(combination) == len(lines_without_no_variants) and
                            combination.attribute_line_id == lines_without_no_variants
                    ):
                        variant.product_template_attribute_value_ids = combination

            # Set containing existing `product.template.attribute.value` combination
            existing_variants = {
                variant.product_template_attribute_value_ids: variant for variant in all_variants
            }

            if not tmpl_id.has_dynamic_attributes():
                # Iterator containing all possible `product.template.attribute.value` combination
                # The iterator is used to avoid MemoryError in case of a huge number of combination.
                all_combinations = itertools.product(*[
                    ptal.product_template_value_ids._only_active() for ptal in lines_without_no_variants
                ])
                # For each possible variant, create if it doesn't exist yet.
                for combination in tmpl_id._filter_combinations_impossible_by_config(
                        all_combinations, ignore_no_variant=True,
                ):
                    if combination in existing_variants:
                        current_variants_to_activate += existing_variants[combination]
                    else:
                        current_variants_to_create.append(tmpl_id._prepare_variant_values(combination))
                        variant_limit = self.env['ir.config_parameter'].sudo().get_param(
                            'product.dynamic_variant_limit', 1000)
                        if len(current_variants_to_create) > int(variant_limit):
                            raise UserError(_(
                                'The number of variants to generate is above allowed limit. '
                                'You should either not generate variants for each combination or generate them on demand from the sales order. '
                                'To do so, open the form view of attributes and change the mode of *Create Variants*.'))
                variants_to_create += current_variants_to_create
                variants_to_activate += current_variants_to_activate

            elif existing_variants:
                variants_combinations = [variant.product_template_attribute_value_ids for variant in
                                         existing_variants.values()]
                current_variants_to_activate += Product.concat(*[existing_variants[possible_combination]
                                                                 for possible_combination in
                                                                 tmpl_id._filter_combinations_impossible_by_config(
                                                                     variants_combinations, ignore_no_variant=True)
                                                                 ])
                variants_to_activate += current_variants_to_activate

            variants_to_unlink += all_variants - current_variants_to_activate

        if variants_to_activate:
            variants_to_activate.write({'active': True})

        if variants_to_create:
            if 'from_merge_product' in self.env.context:
                return True
            else:
                Product.create(variants_to_create)
        self.env.flush_all()
        self.env.invalidate_all()
        return True
