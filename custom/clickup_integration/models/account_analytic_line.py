from odoo import api, models, fields, _


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    _description = "Create task"

    clickup_data_id = fields.Many2many('clickup.data')

    clickup_data_task_id = fields.Char()
