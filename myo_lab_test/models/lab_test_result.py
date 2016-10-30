# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import fields, models

from datetime import datetime


class LabTestResult(models.Model):
    _name = "myo.lab_test.result"

    name = fields.Char('Lab Test Result Code', help="Lab Test Result Code")
    lab_test_type_id = fields.Many2one('myo.lab_test.type', 'Lab Test Type', help="Lab test type")
    patient_id = fields.Many2one('myo.person', 'Patient', help="Patient")
    # 'pathologist' : fields.many2one('clv_professional','Pathologist',help="Pathologist"),
    # 'resulter' : fields.many2one('clv_professional', 'Doctor', help="Doctor who resulted the test"),
    results = fields.Text('Results')
    diagnosis = fields.Text('Diagnosis')
    criterion_ids = fields.One2many(
        'myo.lab_test.criterion',
        'lab_test_result_id',
        'Test Cases'
    )
    date_resulted = fields.Datetime(
        'Date resulted',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    date_analysis = fields.Datetime('Date of the Analysis')
    active = fields.Boolean(
        'Active',
        help="If unchecked, it will allow you to hide the lab test without removing it.",
        default=1
    )

    _sql_constraints = [
        (
            'name_uniq',
            'unique (name)',
            'Error! The Lab Test Code must be unique!'
        )
    ]


class Person(models.Model):
    _inherit = 'myo.person'

    lab_test_result_ids = fields.One2many(
        'myo.lab_test.result',
        'patient_id',
        'Lab Test Results'
    )


class LabTestType(models.Model):
    _inherit = 'myo.lab_test.type'

    lab_test_result_ids = fields.One2many(
        'myo.lab_test.result',
        'lab_test_type_id',
        'Lab Test Results'
    )
