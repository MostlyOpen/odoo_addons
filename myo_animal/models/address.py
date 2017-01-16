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

    animal_ids = fields.One2many(
        'myo.animal',
        'address_id',
        'Animals'
    )
    count_animals = fields.Integer(
        'Number of Animals',
        compute='_compute_count_animals',
        store=True
    )
    count_selected_animals = fields.Integer(
        'Number of Selected Animals',
        compute='_compute_count_selected_animals',
        store=True
    )
    trigger_compute = fields.Boolean(
        'Trigger Compute',
        help="When checked it will trigger the updte of storedcomputet fields.",
        default=False
    )

    @api.depends('animal_ids')
    def _compute_count_animals(self):
        for r in self:
            r.count_animals = len(r.animal_ids)

    @api.depends('animal_ids', 'trigger_compute')
    def _compute_count_selected_animals(self):
        for r in self:
            count_selected_animals = 0
            for animal in r.animal_ids:
                if animal.state == 'selected':
                    count_selected_animals += 1
            r.count_selected_animals = count_selected_animals
            r.trigger_compute = False


class Animal(models.Model):
    _inherit = 'myo.animal'

    address_id = fields.Many2one('myo.address', 'Address', ondelete='restrict')
    animal_phone = fields.Char('Phone', related='address_id.phone')
    mobile_phone = fields.Char('Mobile', related='address_id.mobile')
    animal_email = fields.Char('Email', related='address_id.email')
    address_code = fields.Char('Address Code', related='address_id.code', store=False)
    address_is_residence = fields.Boolean('Address Is Residence', related='address_id.is_residence', store=True)
    address_state = fields.Selection('Address Status', related='address_id.state', store=True)
    address_user_id = fields.Char('Address Responsible', related='address_id.user_id.name', store=True)
    address_category_ids = fields.Char('Address Categories', related='address_id.category_ids.name', store=True)
