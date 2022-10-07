# Copyright 2021
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Clickup Integration Client API',
    'description': """
        Módulo de integração com a plataforma Clickup""",
    "version": "12.0.0.0.0",
    "category": "API Client",
    "website": "",
    'author': 'Cristiano Rodrigues',
    "license": "AGPL-3",
    "depends": ['hr_timesheet_sheet'
                ],
    "data": [
        "security/clickup_data.xml",
        "wizards/import_data_wizard.xml",
        "views/clickup_config.xml",
        "views/clickup_data.xml",
        "views/clickup_menu.xml",
    ],
    'application': True,

}
