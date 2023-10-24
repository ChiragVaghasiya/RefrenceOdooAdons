# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class BalanceReportStage(models.Model):
    _name = 'balance.report.stage'
    _order = 'sequence asc'
    _description = 'Report stages'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(help="Used to order the note stages")

    _sql_constraints = [('report_stage_name_unique', 'unique(name)', 'Stage name already exists')]
