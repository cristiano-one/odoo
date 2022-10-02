import json
import string
from psycopg2 import IntegrityError
import requests
from odoo import _, models, fields
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
    task_priority = fields.Char(string="Priority")

    @staticmethod
    def convert_date_unix(val_unix: int, type: str):
        if val_unix:
            cv = datetime.fromtimestamp(int(val_unix) / 1000)
            if type == 'dt':
                convert = cv.strftime('%d-%m-%Y')
            else:
                convert = cv.strftime('%H:%M:%S')
            return convert

    def import_data(self, res):
        for task in res['tasks']:
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

            creator = task['creator']['username'] if task['creator'] else ''
            data = {
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
                'task_status':  task['status']['status'],
            }
            task_exist = self.search(
                [('task_id', '=', task.get('id'))])

            if not task_exist:
                self.create(data)
            else:
                self.update_data(data)

    def update_data(self, data):
        self.env.cr.execute(
            f""" UPDATE clickup_data SET
                task_id = '{data['task_id']}',
                task_name = '{data['task_name']}',
                task_description = '{data['task_description']}',
                task_date_created = '{data['task_date_created']}',
                task_date_update = '{data['task_date_update']}',
                task_date_closed = '{data['task_date_closed']}',
                task_name_creator = '{data['task_name_creator']}',
                task_assignees = '{data['task_assignees']}',
                task_start_date = '{data['task_start_date']}',
                task_points = '{data['task_points']}',
                task_time_estimate = '{data['task_time_estimate']}',
                task_status = '{data['task_status']}'
                WHERE task_id = '{data.get('id')}' """)
