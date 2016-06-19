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


class MedicamentManufacturer_str(models.Model):
    _name = 'myo.medicament.manufacturer.str'

    name = fields.Char(string='Manufacturer String', required=True)
    manufacturer_id = fields.Many2one('myo.medicament.manufacturer', string='Associated Active Component',
                                      help='Associated Medicament Manufacturer')
    verify = fields.Boolean('Verify')
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'Error! The Manufacturer String must be unique!'),
    ]

    _order = 'name'


class MedicamentManufacturer(models.Model):
    _name = 'myo.medicament.manufacturer'

    name = fields.Char(string='Manufacturer', required=True)
    code = fields.Char(string='Code')
    notes = fields.Text(string='Notes')
    active = fields.Boolean('Active',
                            help="The active field allows you to hide the manufacturer without removing it.",
                            default=1)
    str_ids = fields.One2many('myo.medicament.manufacturer.str', 'manufacturer_id', 'Strings')
    strings = fields.Char(compute="strings_get", string="Strings", store=False)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'Error! The Manufacturer must be unique!'),
        ('code_uniq', 'UNIQUE(code)', u'Error! The Code must be unique!'),
    ]

    _order = 'name'

    @api.multi
    @api.depends('strings')
    def strings_get(self):
        for manufacturer in self:
            strings = ''
            for str_id in manufacturer.str_ids:
                if strings == '':
                    strings = str_id.name
                else:
                    strings = strings + '\n' + str_id.name
        self.strings = strings

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for manufacturer in self:
            result.append((manufacturer.id, '%s {%s}' % (manufacturer.name, manufacturer.code)))
        return result


class MedicamentManufacturer_2(models.Model):
    _inherit = 'myo.medicament.manufacturer'

    medicament_ids = fields.One2many(
        'myo.medicament',
        'manufacturer_id',
        'Medicaments'
    )
