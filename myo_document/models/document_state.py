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
from openerp.exceptions import UserError


class Document(models.Model):
    _inherit = 'myo.document'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('revised', 'Revised'),
        ('waiting', 'Waiting'),
        ('done', 'Done'),
        ('canceled', 'Canceled')
    ], string='State', default='draft', readonly=True, required=True, help="")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [
            ('canceled', 'draft'),
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
        for document in self:
            if document.is_allowed_transition(document.state, new_state):
                document.state = new_state
            else:
                raise UserError('State transition (' + document.state + ', ' + new_state + ') is not allowed!')

    @api.multi
    def action_draft(self):
        for document in self:
            document.change_state('draft')

    @api.multi
    def action_revised(self):
        for document in self:
            document.change_state('revised')

    @api.multi
    def action_waiting(self):
        for document in self:
            document.change_state('waiting')

    @api.multi
    def action_done(self):
        for document in self:
            document.change_state('done')

    @api.multi
    def action_cancel(self):
        for document in self:
            document.change_state('canceled')
