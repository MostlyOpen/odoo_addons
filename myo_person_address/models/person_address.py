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

from datetime import *

from openerp import api, fields, models


class PersonAddress(models.Model):
    _name = 'myo.person.address'

    person_id = fields.Many2one('myo.person', string='Person', help='Person')
    address_id = fields.Many2one('myo.address', 'Address', required=False)
    role_id = fields.Many2one('myo.person.address.role', 'Role', required=False)
    sign_in_date = fields.Date('Sign in date', required=False,
                               default=lambda *a: datetime.now().strftime('%Y-%m-%d'))
    sign_out_date = fields.Date("Sign out date", required=False)
    notes = fields.Text(string='Notes')
    active = fields.Boolean('Active',
                            help="If unchecked, it will allow you to hide the address person without removing it.",
                            default=1)

    _order = "sign_in_date desc"


class Person(models.Model):
    _inherit = 'myo.person'

    person_address_ids = fields.One2many(
        'myo.person.address',
        'person_id',
        'Addresses'
    )


class Address(models.Model):
    _inherit = 'myo.address'

    person_address_ids = fields.One2many(
        'myo.person.address',
        'address_id',
        'Person Addresses'
    )
    count_person_addresss = fields.Integer(
        'Number of Person Addresses',
        compute='_compute_count_person_addresss'
    )

    @api.depends('person_address_ids')
    def _compute_count_person_addresss(self):
        for r in self:
            r.count_person_addresss = len(r.person_address_ids)
