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

{
    'name': 'Lab Test',
    'summary': 'Lab Test Module used in MostlyOpen Solutions.',
    'version': '2.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'http://mostlyopen.org',
    'depends': [
        'myo_base',
        # 'myo_tag',
        # 'myo_annotation',
        'myo_patient'
    ],
    'data': [
        'security/lab_test_security.xml',
        'security/ir.model.access.csv',
        'views/lab_test_unit_view.xml',
        'views/lab_test_criterion_view.xml',
        'views/lab_test_type_view.xml',
        'views/lab_test_request_view.xml',
        'views/lab_test_result_view.xml',
        'views/lab_test_result_state_view.xml',
        'views/lab_test_result_log_view.xml',
        # 'views/tag_view.xml',
        # 'views/annotation_view.xml',
        # 'views/lab_test_log_view.xml',
        # 'views/lab_test_category_log_view.xml',
        'views/lab_test_menu_view.xml',
        'wizard/create_lab_test_view.xml',
        'data/lab_test_seq.xml',
        # 'data/lab_test_data.xml',
    ],
    'demo': [],
    'test': [],
    'init_xml': [],
    'test': [],
    'update_xml': [],
    'installable': True,
    'application': False,
    'active': False,
    'css': [],
}
