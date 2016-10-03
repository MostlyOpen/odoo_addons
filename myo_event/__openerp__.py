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
    'name': 'Event',
    'summary': 'Event Module used in MostlyOpen Solutions.',
    'version': '2.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'http://mostlyopen.org',
    'images': [],
    'depends': [
        'myo_base',
        'myo_tag',
        'myo_annotation',
        # 'myo_person',
        # 'myo_employee',
    ],
    'data': [
        'security/event_security.xml',
        'security/ir.model.access.csv',
        'views/event_view.xml',
        'views/event_category_view.xml',
        'views/tag_view.xml',
        'views/annotation_view.xml',
        'views/event_participant_role_view.xml',
        # 'views/event_address_view.xml',
        # 'views/event_person_view.xml',
        # 'views/event_employee_view.xml',
        'views/event_state_view.xml',
        'views/event_log_view.xml',
        # 'views/event_category_log_view.xml',
        'data/event_seq.xml',
        'views/event_menu_view.xml',
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
