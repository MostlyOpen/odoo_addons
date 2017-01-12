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


class LabTestResult(models.Model):
    _inherit = 'myo.lab_test.result'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('started', 'Started'),
        ('transcribed', 'Transcribed'),
        ('released', 'Released'),
        ('canceled', 'Canceled'),
    ], string='Status', default='draft', readonly=True, required=True, help="")

    @api.multi
    def change_state(self, new_state):
        for lab_test_result in self:
            lab_test_result.state = new_state

    @api.multi
    def action_draft(self):
        for lab_test_result in self:
            lab_test_result.change_state('draft')

    @api.multi
    def action_started(self):
        for lab_test_result in self:
            lab_test_result.change_state('started')

    @api.multi
    def action_transcribed(self):
        for lab_test_result in self:
            lab_test_result.change_state('transcribed')

    @api.multi
    def action_select(self):
        for lab_test_result in self:
            lab_test_result.change_state('released')

    @api.multi
    def action_cancel(self):
        for lab_test_result in self:
            lab_test_result.change_state('canceled')
