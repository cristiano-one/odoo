from odoo import api, models, fields, _


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    _description = "Create task"


@api.model
def create(self, values):
    if not self.env.context.get('sheet_create') and 'sheet_id' in values:
        del values['sheet_id']
    res = super(AccountAnalyticLine, self).create(values)
    res._compute_sheet()
    return res
