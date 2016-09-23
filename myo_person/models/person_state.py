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

from datetime import *


class Address(models.Model):
    _inherit = 'myo.person'

    state = fields.Selection([('draft', 'Draft'),
                              ('revised', 'Revised'),
                              ('waiting', 'Waiting'),
                              ('selected', 'Selected'),
                              ('unselected', 'Unselected'),
                              ('canceled', 'Canceled')
                              ], string='Status', default='draft', readonly=True, required=True, help="")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('canceled', 'draft'),
                   ('draft', 'revised'),
                   ('waiting', 'revised'),
                   ('selected', 'revised'),
                   ('unselected', 'revised'),
                   ('revised', 'waiting'),
                   ('revised', 'selected'),
                   ('waiting', 'selected'),
                   ('unselected', 'selected'),
                   ('revised', 'unselected'),
                   ('waiting', 'unselected'),
                   ('selected', 'unselected'),
                   ('draft', 'canceled'),
                   ('revised', 'canceled')]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for person in self:
            if person.is_allowed_transition(person.state, new_state):
                person.state = new_state
            else:
                raise Warning('Warning. State transition (' + person.state + ', ' + new_state + ') is not allowed!')

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
    def action_select(self):
        # self.state = 'selected'
        self.change_state('selected')

    @api.one
    def action_unselect(self):
        # self.state = 'unselected'
        self.change_state('unselected')

    @api.one
    def action_cancel(self):
        # self.state = 'canceled'
        self.change_state('canceled')
