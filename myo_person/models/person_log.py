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


class PersonLog(models.Model):
    _name = 'myo.person.log'

    person_id = fields.Many2one('myo.person', 'Person', required=True, ondelete='cascade')
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


class Person(models.Model):
    _inherit = 'myo.person'

    log_ids = fields.One2many('myo.person.log', 'person_id', 'Person Log',
                              readonly=True)
    active_log = fields.Boolean(
        'Active Log',
        help="If unchecked, it will allow you to disable the log without removing it.",
        default=True
    )

    @api.one
    def insert_myo_person_log(self, person_id, values, action, notes):
        active_log = False
        if 'active_log' in values:
            active_log = values['active_log']
        if self.active_log or active_log:
            vals = {
                'person_id': person_id,
                'values': values,
                'action': action,
                'notes': notes,
            }
            self.pool.get('myo.person.log').create(self._cr, self._uid, vals)

    @api.multi
    def write(self, values):
        action = 'write'
        # notes = values.keys()
        # notes = values.keys() + values.values()
        notes = False
        for person in self:
            person.insert_myo_person_log(person.id, values, action, notes)
        return super(Person, self).write(values)

    @api.model
    def create(self, values):
        action = 'create'
        notes = False
        record = super(Person, self).create(values)
        record.insert_myo_person_log(record.id, values, action, notes)
        return record
