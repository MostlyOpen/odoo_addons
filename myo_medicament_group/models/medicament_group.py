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


class MedicamentGroup(models.Model):
    _name = 'myo.medicament.group'

    name = fields.Char('Name', select=1, required=True, help='Medicament Group Name')
    alias = fields.Char('Alias', help='Common name that the Medicament Group is referred')
    code = fields.Char(string='Medicament Group Code', required=False)
    notes = fields.Text(string='Notes')
    date_inclusion = fields.Datetime("Inclusion Date", required=False, readonly=False,
                                     default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    active = fields.Boolean('Active',
                            help="If unchecked, it will allow you to hide the medicament group without removing it.",
                            default=1)
    medicament_name = fields.Char(string='Medicament Name')
    concentration = fields.Char(string='Concentration')
    pres_form_id = fields.Many2one('myo.medicament.form', string='Presentation Form',
                                   help='Medicament form, such as tablet or gel')

    _order = 'name'


class MedicamentGroup_2(models.Model):
    _inherit = 'myo.medicament.group'

    active_component_id = fields.Many2one('myo.medicament.active_component',
                                          string='Active Component',
                                          help='Medicament Active Component')
    active_component_name = fields.Char(related='active_component_id.name',
                                        string='Related Active Component')
