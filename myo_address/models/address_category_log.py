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


class AddressCategoryLog(models.Model):
    _name = 'myo.address.category.log'

    address_category_id = fields.Many2one('myo.address.category',
                                          'Address Category',
                                          required=True,
                                          ondelete='cascade')
    user_id = fields.Many2one('res.users', 'User', required=True)
    date_log = fields.Datetime("Log Date", required=True)
    values = fields.Text(string='Values')
    action = fields.Char(string='Action')
    notes = fields.Text(string='Notes')

    _order = "date_log desc"

    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'date_log': lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }


class AddressCategory(models.Model):
    _inherit = 'myo.address.category'

    log_ids = fields.One2many('myo.address.category.log', 'address_category_id', 'Address Category Log',
                              readonly=True)
    active_log = fields.Boolean(
        'Active Log',
        help="If unchecked, it will allow you to disable the log without removing it.",
        default=True
    )

    @api.one
    def insert_myo_address_category_log(self, address_category_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            vals = {
                'address_category_id': address_category_id,
                'values': values,
                'action': action,
                'notes': notes,
            }
            self.pool.get('myo.address.category.log').create(self._cr, self._uid, vals)

    @api.multi
    def write(self, values):
        action = 'write'
        # notes = values.keys()
        # notes = values.keys() + values.values()
        notes = False
        for address_category in self:
            address_category.insert_myo_address_category_log(address_category.id, values, action, notes)
        return super(AddressCategory, self).write(values)

    @api.model
    def create(self, values):
        action = 'create'
        notes = False
        record = super(AddressCategory, self).create(values)
        record.insert_myo_address_category_log(record.id, values, action, notes)
        return record
