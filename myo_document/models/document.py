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

from datetime import datetime

from openerp import fields, models


class Document(models.Model):
    _name = "myo.document"

    name = fields.Char('Document Code', help="Document Code")
    date_requested = fields.Datetime('Date requested',
                                     default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_document = fields.Datetime('Document Date')
    responsible = fields.Many2one('res.users', 'Document Responsible', required=False, readonly=False)
    notes = fields.Text(string='Notes')
    active = fields.Boolean('Active',
                            help="If unchecked, it will allow you to hide the document without removing it.",
                            default=1)

    _sql_constraints = [('name_uniq', 'unique (name)', 'Error! The Document Code must be unique!')]

    _order = 'name'
