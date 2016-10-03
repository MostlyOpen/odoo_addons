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
from openerp.exceptions import Warning


class Event(models.Model):
    _inherit = 'myo.event'

    state = fields.Selection([('draft', 'Draft'),
                              ('revised', 'Revised'),
                              ('waiting', 'Waiting'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')
                              ], string='Status', default='draft', readonly=True, required=True, help="")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('canceled', 'draft'),
                   ('draft', 'revised'),
                   ('waiting', 'revised'),
                   ('done', 'revised'),
                   ('revised', 'waiting'),
                   ('revised', 'done'),
                   ('waiting', 'done'),
                   ('draft', 'canceled'),
                   ('revised', 'canceled')]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for event in self:
            if event.is_allowed_transition(event.state, new_state):
                event.state = new_state
            else:
                raise Warning('Warning. State transition (' + event.state + ', ' + new_state + ') is not allowed!')

    @api.one
    def action_draft(self):
        # self.state = 'draft'
        self.change_state('draft')

    @api.one
    def action_revised(self):
        # self.state = 'revised'
        self.change_state('revised')

    @api.one
    def action_waiting(self):
        # self.state = 'waiting'
        self.change_state('waiting')

    @api.one
    def action_done(self):
        # self.state = 'done'
        self.change_state('done')

    @api.one
    def action_cancel(self):
        # self.state = 'canceled'
        self.change_state('canceled')
