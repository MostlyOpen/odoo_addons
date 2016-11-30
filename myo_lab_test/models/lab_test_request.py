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


class LabTestRequest(models.Model):
    _name = 'myo.lab_test.request'

    name = fields.Char('Lab Test Result Code', help="Lab Test Result Code")
    lab_test_type_id = fields.Many2one('myo.lab_test.type', 'Lab Test Type')
    patient_id = fields.Many2one('myo.person', 'Patient')
    date = fields.Datetime(
        'Date',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    lab_test_result_id = fields.Many2one('myo.lab_test.result', 'Lab Test Result')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('tested', 'Tested'),
        ('canceled', 'Canceled'),
    ], 'Status', default='draft', readonly=True)


class Person(models.Model):
    _inherit = 'myo.person'

    lab_test_request_ids = fields.One2many(
        'myo.lab_test.request',
        'patient_id',
        'Lab Test Requests'
    )


class LabTestType(models.Model):
    _inherit = 'myo.lab_test.type'

    lab_test_request_ids = fields.One2many(
        'myo.lab_test.request',
        'lab_test_type_id',
        'Lab Test Requests'
    )
