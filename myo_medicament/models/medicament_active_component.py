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


class MedicamentActiveComponent_str(models.Model):
    _name = 'myo.medicament.active_component.str'

    name = fields.Char(string='Active Component String', required=True)
    active_component_id = fields.Many2one('myo.medicament.active_component', string='Associated Active Component',
                                          help='Associated Medicament Active Component')
    verify = fields.Boolean('Verify')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'Error! The Active Component String must be unique!'),
    ]

    _order = 'name'


class MedicamentActiveComponent(models.Model):
    _name = 'myo.medicament.active_component'

    name = fields.Char(string='Active Component', required=True)
    code = fields.Char(string='Code')
    notes = fields.Text(string='Notes')
    active = fields.Boolean('Active',
                            help="The active field allows you to hide the active component without removing it.",
                            default=1)
    str_ids = fields.One2many('myo.medicament.active_component.str', 'active_component_id', 'Strings')
    strings = fields.Char(compute="strings_get", string="Strings", store=False)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'Error! The Active Component must be unique!'),
        ('code_uniq', 'UNIQUE(code)', u'Error! The Code must be unique!'),
    ]

    _order = 'name'

    @api.multi
    @api.depends('strings')
    def strings_get(self):
        for active_component in self:
            strings = ''
            for str_id in active_component.str_ids:
                if strings == '':
                    strings = str_id.name
                else:
                    strings = strings + '\n' + str_id.name
        self.strings = strings

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for active_component in self:
            result.append((active_component.id, '%s {%s}' % (active_component.name, active_component.code)))
        return result


class MedicamentActiveComponent_2(models.Model):
    _inherit = 'myo.medicament.active_component'

    medicament_ids = fields.One2many(
        'myo.medicament',
        'active_component_id',
        'Medicaments'
    )
