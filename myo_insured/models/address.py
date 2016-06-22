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


class Address(models.Model):
    _inherit = 'myo.address'

    insured_ids = fields.One2many(
        'myo.insured',
        'address_id',
        'Insureds'
    )


class Insured(models.Model):
    _inherit = 'myo.insured'

    address_id = fields.Many2one('myo.address', 'Insured Address', ondelete='restrict')
    insured_phone = fields.Char('Insured Phone', related='address_id.phone')
    mobile_phone = fields.Char('Insured Mobile', related='address_id.mobile')
    insured_email = fields.Char('Insured Email', related='address_id.email')
