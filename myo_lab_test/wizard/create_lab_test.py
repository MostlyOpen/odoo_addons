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

from datetime import datetime


class CreateLabTest(models.TransientModel):
    _name = 'myo.lab_test.create'

    def _default_lab_test_request_ids(self):
        return self._context.get('active_ids')
    lab_test_request_ids = fields.Many2many(
        'myo.lab_test.request',
        string='Lab Test Requests',
        default=_default_lab_test_request_ids
    )
    employee_id = fields.Many2one('hr.employee', string='Received by')
    date_received = fields.Datetime(
        'Received Date',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    @api.multi
    def create_lab_test(self):

        self.lab_test_request_ids = self._context.get('active_ids')
        lab_obj = self.env['myo.lab_test.result']

        lab_test_type_model = self.env['myo.lab_test.type']
        lab_test_type_id_EPC17 = lab_test_type_model.search([
            ('code', '=', 'EPC17'),
        ]).id
        lab_test_type_id_EPI17 = lab_test_type_model.search([
            ('code', '=', 'EPI17'),
        ]).id
        lab_test_type_ECP17 = lab_test_type_model.search([
            ('code', '=', 'ECP17'),
        ])
        lab_test_type_id_ECP17 = lab_test_type_model.search([
            ('code', '=', 'ECP17'),
        ]).id

        for test_obj in self.lab_test_request_ids:
            test_report_data = {}
            test_cases = []
            if test_obj.state == 'draft':
                test_report_data['name'] = test_obj.name

                # todo: Verify!!!!!!!!!
                #
                if (test_obj.lab_test_type_id.id == lab_test_type_id_EPC17) or \
                   (test_obj.lab_test_type_id.id == lab_test_type_id_EPI17):
                    test_report_data['lab_test_type_id'] = lab_test_type_id_ECP17
                    lab_test_type = lab_test_type_ECP17
                else:
                    test_report_data['lab_test_type_id'] = test_obj.lab_test_type_id.id
                    lab_test_type = test_obj.lab_test_type_id
                #
                # End Verify

                # test_report_data['lab_test_type_id'] = test_obj.lab_test_type_id.id
                test_report_data['patient_id'] = test_obj.patient_id.id
                # test_report_data['date_requested'] = test_obj.date_requested

                # for criterion in test_obj.lab_test_type_id.criterion_ids:
                for criterion in lab_test_type.criterion_ids:
                    test_cases.append((0, 0, {'code': criterion.code,
                                              'name': criterion.name,
                                              'sequence': criterion.sequence,
                                              'normal_range': criterion.normal_range,
                                              'unit_id': criterion.unit_id.id,
                                              }))
                test_report_data['criterion_ids'] = test_cases
                lab_id = lab_obj.create(test_report_data)
                test_obj.state = 'tested'
                test_obj.lab_test_result_id = lab_id
                test_obj['employee_id'] = self.employee_id
                test_obj['date_received'] = self.date_received

        return {
            'domain': "[]",
            'name': 'Lab Test Results',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'myo.lab_test.result',
            'type': 'ir.actions.act_window'
        }
