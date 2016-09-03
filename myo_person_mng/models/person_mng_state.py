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


class PersonManagement(models.Model):
    _inherit = 'myo.person.mng'

    state = fields.Selection([('draft', 'Draft'),
                              ('revised', 'Revised'),
                              ('waiting', 'Waiting'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')
                              ], string='Status', default='draft', readonly=True, required=True, help="")

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_revised(self):
        self.state = 'revised'

    @api.one
    def action_waiting(self):
        self.state = 'waiting'

    @api.one
    def action_done(self):
        self.state = 'done'

    @api.one
    def action_cancel(self):
        self.state = 'canceled'
