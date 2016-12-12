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


class Address(models.Model):
    _inherit = 'myo.address'

    count_patients = fields.Integer(
        'Number of Patients',
        compute='_compute_count_patients',
        store=True
    )

    @api.depends('person_ids', 'trigger_compute')
    def _compute_count_patients(self):
        for r in self:
            count_patients = 0
            for person in r.person_ids:
                if person.is_patient is True:
                    count_patients += 1
            r.count_patients = count_patients
            r.trigger_compute = False
