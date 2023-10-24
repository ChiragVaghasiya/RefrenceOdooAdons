from odoo import models, fields, api

class ResUsers(models.Model):
	_inherit = 'res.users'

	is_applicable_stock_adjust_pos = fields.Boolean('Is Applicable to Adjust Stock in POS')