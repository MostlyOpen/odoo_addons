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


class Pharmacy(models.Model):
    _name = 'myo.pharmacy'

    name = fields.Char('Pharmacy', required=True, translate=False)
    alias = fields.Char('Alias', help='Common name that the Pharmacy is referred')
    code = fields.Char(size=64, string='Pharmacy Code', required=False)
    notes = fields.Text(string='Notes')
    date_inclusion = fields.Datetime("Inclusion Date", required=False, readonly=False,
                                     default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    active = fields.Boolean('Active',
                            help="If unchecked, it will allow you to hide the pharmacy without removing it.",
                            default=1)

    _order = 'name'

    _sql_constraints = [('code_uniq', 'unique(code)', u'Error! The Pharmacy Code must be unique!')]
