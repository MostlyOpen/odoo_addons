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

from openerp.osv import osv


class CreateLabTest(osv.osv_memory):
    _name = 'myo.lab_test.create'

    def create_lab_test(self, cr, uid, ids, context={}):

        # data = ids

        print('>>>>>', self, ids, context.get('active_id'))
        test_request_obj = self.pool.get('myo.lab_test.patient')
        lab_obj = self.pool.get('myo.lab_test')

        test_report_data = {}
        test_cases = []
        test_obj = test_request_obj.browse(cr, uid, context.get('active_id'), context=context)
        if test_obj.state == 'tested':
            raise osv.except_osv(('UserError'), ('Test Report already created.'))
        test_report_data['lab_test_type_id'] = test_obj.name.id
        test_report_data['patient_id'] = test_obj.patient_id.id
        # test_report_data['requestor'] = test_obj.doctor_id.id
        test_report_data['date_requested'] = test_obj.date

        for criterion in test_obj.name.criterion_ids:
            test_cases.append((0, 0, {'name': criterion.name,
                                      'sequence': criterion.sequence,
                                      'normal_range': criterion.normal_range,
                                      'unit_id': criterion.unit_id.id
                                      }))
        test_report_data['criterion_ids'] = test_cases
        lab_id = lab_obj.create(cr, uid, test_report_data, context=context)
        test_request_obj.write(cr, uid, context.get('active_id'), {'state': 'tested', 'lab_test_id': lab_id})
        return {
            'domain': "[('id','=', " + str(lab_id) + ")]",
            'name': 'Lab Test Report',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'myo.lab_test',
            'type': 'ir.actions.act_window'
        }
