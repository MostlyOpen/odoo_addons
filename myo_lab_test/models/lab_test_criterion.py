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


class LabTestTypeCriterion(models.Model):
    _name = "myo.lab_test.criterion"

    name = fields.Char('Test')
    # result = fields.Text('Results')
    result = fields.Char('Results')
    normal_range = fields.Text('Normal Range')
    # outcome_ids = fields.Many2many('myo.lab_test.outcome',
    #                                'myo_lab_test_outcome_rel',
    #                                'criterion_id',
    #                                'outcome_id',
    #                                'Outcomes')
    # valid_values = fields.Text('Valid Values')
    unit_id = fields.Many2one('myo.lab_test.unit', 'Unit')
    lab_test_type_id = fields.Many2one('myo.lab_test.type', 'Test Type')
    lab_test_result_id = fields.Many2one('myo.lab_test.result', 'Test Cases')
    sequence = fields.Integer(
        'Sequence',
        default=10
    )

    _order = "sequence"
