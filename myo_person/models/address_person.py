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


class AddressPerson(models.Model):
    _name = 'myo.address.person'

    address_id = fields.Many2one('myo.address', 'Address', required=False)
    person_id = fields.Many2one('myo.person', string='Person', help='Person')
    role_id = fields.Many2one('myo.address.person.role', 'Role', required=False)
    sign_in_date = fields.Date('Sign in date', required=False,
                               default=lambda *a: datetime.now().strftime('%Y-%m-%d'))
    sign_out_date = fields.Date("Sign out date", required=False)
    notes = fields.Text(string='Notes')
    active = fields.Boolean('Active',
                            help="If unchecked, it will allow you to hide the address person without removing it.",
                            default=1)

    _order = "sign_in_date desc"


class Address(models.Model):
    _inherit = 'myo.address'

    address_person_ids = fields.One2many(
        'myo.address.person',
        'address_id',
        'Address Persons'
    )
    count_address_persons = fields.Integer(
        'Number of Address Persons',
        compute='_compute_count_address_persons'
    )

    @api.depends('address_person_ids')
    def _compute_count_address_persons(self):
        for r in self:
            r.count_address_persons = len(r.address_person_ids)


class Person(models.Model):
    _inherit = 'myo.person'

    address_person_ids = fields.One2many(
        'myo.address.person',
        'person_id',
        'Addresses'
    )
