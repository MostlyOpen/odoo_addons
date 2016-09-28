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

from datetime import *

from openerp import fields, models


class Annotation(models.Model):
    _name = 'myo.annotation'

    name = fields.Char('Subject', index=True, required=True)
    code = fields.Char('Code', required=False)
    author = fields.Many2one('res.users', 'Author', required=True, readonly=True,
                             default=lambda self: self._uid)
    date = fields.Datetime("Date", required=True, readonly=True,
                           default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    body = fields.Text(string='Body')
    active = fields.Boolean('Active',
                            help="If unchecked, it will allow you to hide the Annotation without removing it.",
                            default=1)

    _sql_constraints = [
        ('uniq_annotation_code', 'unique(code)', "Error! The Annotation Code must be unique!"),
    ]

    _order = "date desc"
