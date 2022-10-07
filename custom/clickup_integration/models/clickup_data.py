import json
import string
from psycopg2 import IntegrityError
import requests
from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class ClickupData(models.Model):
    _name = "clickup.data"
    _description = "Get the task data from the list"

    task_name = fields.Char(string="Nome da Task")
    task_id = fields.Char(string="Task Id")
    task_description = fields.Char(string="Description")
    task_status = fields.Char(string="Status")
    task_date_created = fields.Char(string="Data Created")
    task_date_update = fields.Char(string="Data Update")
    task_date_closed = fields.Char(string="Data Closed")
    task_arquived = fields.Boolean(string="Arquived")
    task_name_creator = fields.Char(string="Name Creator")
    task_assignees = fields.Char(string="Name Assignees")
    task_start_date = fields.Char(string="Start Date")
    task_points = fields.Char(string="Points")
    task_time_estimate = fields.Char(string="Time Estimate")
    task_time_spent = fields.Char(string="Time Espent")
    task_priority = fields.Char(string="Priority")

    @staticmethod
    def convert_date_unix(val_unix: int, type: str):
        if val_unix:
            cv = datetime.fromtimestamp(int(val_unix) / 1000)
            if type == 'dt':
                convert = cv.strftime('%Y-%m-%d')
            else:
                convert = cv.strftime('%H:%M')
            return convert

    def _get_data_imported_fields(self, task):
        description = task['description'].replace(
            "'", "") if task['description'] else ""
        assignees = task['assignees'][0]['username'] \
            if task['assignees'] else ''
        task_date_created = self.convert_date_unix(
            task.get('date_created'), 'dt')
        task_date_update = self.convert_date_unix(
            task.get('date_updated'), 'dt')
        task_date_closed = self.convert_date_unix(
            task.get('date_closed'), 'dt')
        task_start_date = self.convert_date_unix(
            task.get('start_date'), 'dt')
        task_time_estimate = self.convert_date_unix(
            task.get('time_estimate'), 'hr')
        task_time_spent = self.convert_date_unix(
            task.get('time_spent'), 'hr')

        creator = task['creator']['username'] if task['creator'] else ''
        return {
            'task_id':  task.get('id'),
            'task_name':  task.get('name'),
            'task_description': description,
            'task_date_created': task_date_created,
            'task_date_update': task_date_update,
            'task_date_closed': task_date_closed,
            'task_name_creator': creator,
            'task_assignees': assignees,
            'task_start_date': task_start_date,
            'task_points': task.get('points'),
            'task_time_estimate': task_time_estimate,
            'task_time_spent': task_time_spent,
            'task_status':  task['status']['status']
        }

    def import_data(self, res):
        for task in res['tasks']:
            data = self._get_data_imported_fields(task)
            task_id = self.search(
                [('task_id', '=', data.get('task_id'))])

            if not task_id and data.get('task_id'):
                self.create(data)
            else:
                task_id.update(data)

            self.create_timesheet(data)

    def create_timesheet(self, data):
        vals = self._get_data_timesheet_fields(data)
        account_analytic_line_id = self.env['account.analytic.line'].search(
            [('clickup_data_task_id', '=', data['task_id'])])
        if not account_analytic_line_id:
            self.env['account.analytic.line'].create(vals)
        else:
            if account_analytic_line_id:
                account_analytic_line_id.write(vals)

    @api.model
    def _get_data_timesheet_fields(self, data):
        """ Set values timesheet"""

        if data['task_time_spent']:
            task_time = data['task_time_spent'].replace(
                ':', '')
            task_time_spent = float(task_time) / 100
        else:
            task_time_spent = None
        return {
            'clickup_data_task_id': data['task_id'],
            'name': data['task_name'],
            'date': data['task_date_created'],  # '2022-10-01',
            'unit_amount': task_time_spent,
            # 'user_id': 2,
            # 'employee_id': False,
            # 'department_id': False,
            # 'company_id': 1,
            # 'task_id': False,
            'project_id': 4,
            # 'sheet_id': False
        }
