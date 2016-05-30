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


class MedicamentList(models.Model):
    _name = 'myo.medicament.list'

    name = fields.Char('Medicament List Name', required=True, translate=True)
    alias = fields.Char('Alias', help='Common name that the Medicament List is referred')
    code = fields.Char(string='Medicament List Code', required=False)
    # partner_id = fields.Many2one('res.partner', 'Partner')
    # ext_code = fields.Char(string='External Medicament List Code', required=False)
    notes = fields.Text(string='Notes')
    date_inclusion = fields.Datetime("Inclusion Date", required=False, readonly=False,
                                     default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    active = fields.Boolean('Active',
                            help="The active field allows you to hide the medicament list without removing it.",
                            default=1)

    _sql_constraints = [('code_uniq', 'unique(code)', u'Error! The Medicament List Code must be unique!')]

    _order = 'name'
