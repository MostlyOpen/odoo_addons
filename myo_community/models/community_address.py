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

from openerp import fields, models


class CommunityAddress(models.Model):
    _name = 'myo.community.address'

    community_id = fields.Many2one('myo.community', string='Community',
                                   help='Community', required=False)
    address_id = fields.Many2one('myo.address', string='Address')
    role = fields.Many2one('myo.community.member.role', 'Role', required=False)
    notes = fields.Text(string='Notes')
    active = fields.Boolean('Active',
                            help="If unchecked, it will allow you to hide the community address without removing it.",
                            default=1)


class Community(models.Model):
    _inherit = 'myo.community'

    address_ids = fields.One2many(
        'myo.community.address',
        'community_id',
        'Addresses'
    )


class Address(models.Model):
    _inherit = 'myo.address'

    community_address_ids = fields.One2many(
        'myo.community.address',
        'address_id',
        'Community Addresses'
    )
