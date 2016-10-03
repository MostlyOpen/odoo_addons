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


class Event(models.Model):
    _name = "myo.event"

    _order = "sequence, date_start, name, id"

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 u'%s [%s]' % (record.name, record.code)
                 ))
        return result

    name = fields.Char(string='Event Title', required=True, index=True)
    description = fields.Html(string='Description')
    code = fields.Char(string='Event Code')
    sequence = fields.Integer(
        string='Sequence', index=True, default=10,
        help="Gives the sequence order when displaying a list of events.")
    planned_hours = fields.Float(
        string='Planned Hours',
        help='Estimated time (in hours) to do the event.'
    )
    date_inclusion = fields.Datetime('Inclusion Date', default=fields.Datetime.now)
    date_start = fields.Datetime(string='Starting Date', index=True, copy=False)
    date_foreseen = fields.Datetime(string='Foreseen Date', index=True, copy=False)
    date_deadline = fields.Date(string='Deadline', index=True, copy=False)
    user_id = fields.Many2one('res.users', 'Event Responsible')
    notes = fields.Html(string='Notes')
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(
        'Active',
        help="If unchecked, it will allow you to hide the event without removing it.",
        default=True
    )

    _sql_constraints = [
        (
            'code_uniq',
            'UNIQUE (code)',
            'Error! The Code must be unique!'
        ),
    ]
