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

from openerp import api, fields, models


class CreateLabTest(models.TransientModel):
    _name = 'myo.lab_test.create'

    lab_test_patient_ids = fields.Many2many('myo.lab_test.patient', string='Lab Test Patients')

    @api.multi
    def create_lab_test(self):

        self.lab_test_patient_ids = self._context.get('active_ids')
        lab_obj = self.env['myo.lab_test']

        for test_obj in self.lab_test_patient_ids:
            test_report_data = {}
            test_cases = []
            if test_obj.state == 'draft':
                test_report_data['name'] = test_obj.code
                test_report_data['lab_test_type_id'] = test_obj.name.id
                test_report_data['patient_id'] = test_obj.patient_id.id
                test_report_data['date_requested'] = test_obj.date

                for criterion in test_obj.name.criterion_ids:
                    test_cases.append((0, 0, {'name': criterion.name,
                                              'sequence': criterion.sequence,
                                              'normal_range': criterion.normal_range,
                                              'unit_id': criterion.unit_id.id
                                              }))
                test_report_data['criterion_ids'] = test_cases
                lab_id = lab_obj.create(test_report_data)
                test_obj.state = 'tested'
                test_obj.lab_test_id = lab_id
        return {
            'domain': "[]",
            'name': 'Lab Test Report',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'myo.lab_test',
            'type': 'ir.actions.act_window'
        }
