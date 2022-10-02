
from email.policy import default
import requests
from datetime import datetime
from odoo.exceptions import UserError
from odoo import _, api, fields, models


class MessageBox(models.TransientModel):
    _name = "import.data.wizard"
    _description = "Import data Clickup"

    list_id = fields.Char("List ID", required=True)
    archived = fields.Boolean("Archived", default=False)

    @staticmethod
    def convert_date_unix(date_unix: int):
        if date_unix:
            dt = int(date_unix) / 1000
            convert = datetime.fromtimestamp(
                dt).strftime('%d-%m-%Y')
            return convert

    def clickup_date(self):
        config_id = self.env['clickup.config'].search(
            [('clickup_authenticated', '=', True)])
        type_data = "list/"
        arq = 'false' if not self.archived else 'true'
        params = f"/task?archived={arq}&include_closed=true"
        http = self.url()
        url = f"{http}{type_data}{self.list_id}{params}"

        header = {
            "Authorization": config_id.token,
            'Content-Type': 'multipart/form-data'
        }
        try:
            r = requests.get(url, headers=header)
        except Exception:
            raise UserError(
                _('Connection error/Max retries exceeded with url: /api/v2/'))

        res = r.json()

        if res.get('err'):
            raise UserWarning(_('Import failed'))
        else:
            self.env["clickup.data"].import_data(res)
            # UserWarning(_('Successfully imported'))

    @staticmethod
    def url():
        return "https://api.clickup.com/api/v2/"
