
import requests
from odoo import models, fields


class ClickupConfig(models.Model):
    _name = "clickup.config"
    _description = "Configuraton initial"

    token = fields.Char(string='Token', required=True)
    client_id = fields.Char(string='Client Id')
    client_secret = fields.Char(string='Client Secret')
    clickup_authenticated = fields.Boolean(default=False)

    def clickup_validate(self):
        token = self.token 
        type_data = "list/"  # list ou task
        id_find = "187103630"  # "187103630" # id pode ser um list_id ou task_id
        params = "/task?archived=false"

        url = "https://api.clickup.com/api/v2/"
        header = {
            "contentType": "application/json",
            "Authorization": token,
        }
        r = requests.get(url+type_data+id_find+params, headers=header)

        res = r.json()

        if not res.get('err'):
            self.clickup_authenticated = True
        else:
            self.clickup_authenticated = False
