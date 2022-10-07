
import requests
from odoo import api, models, fields


class ClickupConfig(models.TransientModel):
    _name = "clickup.config"
    _inherit = "res.config.settings"
    _description = "Configuraton initial"

    clickup_client_id = fields.Char(
        string='Client Id',
        config_parameter='clickup_client_id'
    )
    clickup_client_secret = fields.Char(
        string='Client Secret',
        config_parameter='clickup_client_secret'
    )
    clickup_token = fields.Char(
        string='Token',
        required=True,
        config_parameter='clickup_token')
    clickup_authenticated = fields.Boolean(
        default=False,
        config_parameter='clickup_authenticated'
    )

    def clickup_validate(self):
        # TODO Lembrar do fazer update com mais opções
        token = self.clickup_token
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

    @api.model
    def get_values(self):
        res = super(ClickupConfig, self).get_values()
        clickup_config_id = self.search(
            [('clickup_authenticated', '=', True)], limit=1)
        res.update(
            clickup_token=clickup_config_id.clickup_token,
            clickup_authenticated=clickup_config_id.clickup_authenticated,
        )
        return res
