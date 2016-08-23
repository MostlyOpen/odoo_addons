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

from datetime import *


class AddressLog(models.Model):
    _name = 'myo.address.log'

    address_id = fields.Many2one('myo.address', 'Address', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', 'User', required=True)
    date_log = fields.Datetime("Log Date", required=True)
    values = fields.Text(string='Values')
    notes = fields.Text(string='Notes')

    _order = "date_log desc"

    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'date_log': lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }


class Address(models.Model):
    _inherit = 'myo.address'

    log_ids = fields.One2many('myo.address.log', 'address_id', 'Address Log',
                              readonly=True)
    active_log = fields.Boolean(
        'Active Log',
        help="If unchecked, it will allow you to disable the log without removing it.",
        default=True
    )

    @api.one
    def insert_myo_address_log(self, address_id, values, notes):
        active_log = False
        if 'active_log' in values:
            active_log = values['active_log']
        if self.active_log or active_log:
            vals = {
                'address_id': address_id,
                'values': values,
                'notes': notes,
            }
            self.pool.get('myo.address.log').create(self._cr, self._uid, vals)

    @api.multi
    def write(self, values):
        # notes = values.keys()
        # notes = values.keys() + values.values()
        notes = False
        self.insert_myo_address_log(self.id, values, notes)
        return super(Address, self).write(values)

    @api.model
    def create(self, values):
        notes = False
        record = super(Address, self).create(values)
        record.insert_myo_address_log(record.id, values, notes)
        return record
