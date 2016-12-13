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

    person_ids = fields.One2many(
        'myo.person',
        'address_id',
        'Persons'
    )
    count_persons = fields.Integer(
        'Number of Persons',
        compute='_compute_count_persons',
        store=True
    )
    count_selected_persons = fields.Integer(
        'Number of Selected Persons',
        compute='_compute_count_selected_persons',
        store=True
    )
    trigger_compute = fields.Boolean(
        'Trigger Compute',
        help="When checked it will trigger the updte of storedcomputet fields.",
        default=False
    )

    @api.depends('person_ids')
    def _compute_count_persons(self):
        for r in self:
            r.count_persons = len(r.person_ids)

    @api.depends('person_ids', 'trigger_compute')
    def _compute_count_selected_persons(self):
        for r in self:
            count_selected_persons = 0
            for person in r.person_ids:
                if person.state == 'selected':
                    count_selected_persons += 1
            r.count_selected_persons = count_selected_persons
            r.trigger_compute = False


class Person(models.Model):
    _inherit = 'myo.person'

    address_id = fields.Many2one('myo.address', 'Address', ondelete='restrict')
    person_phone = fields.Char('Phone', related='address_id.phone')
    mobile_phone = fields.Char('Mobile', related='address_id.mobile')
    person_email = fields.Char('Email', related='address_id.email')
    address_code = fields.Char('Address Code', related='address_id.code', store=False)
    address_is_residence = fields.Boolean('Address Is Residence', related='address_id.is_residence', store=True)
    address_state = fields.Selection('Address Status', related='address_id.state', store=True)
    address_user_id = fields.Char('Address Responsible', related='address_id.user_id.name', store=True)
    address_category_ids = fields.Char('Address Categories', related='address_id.category_ids.name', store=True)
