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

from openerp import fields, models


class AnimalSpecies(models.Model):
    _name = 'myo.animal.species'

    name = fields.Char(string='Species', required=True)
    code = fields.Char(string='Code')
    notes = fields.Text(string='Notes')
    active = fields.Boolean('Active',
                            help="The active field allows you to hide the species without removing it.",
                            default=1)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'Error! The Species must be unique!'),
        ('code_uniq', 'UNIQUE(code)', u'Error! The Code must be unique!'),
    ]

    _order = 'name'

    # @api.multi
    # @api.depends('name', 'code')
    # def name_get(self):
    #     result = []
    #     for species in self:
    #         result.append((species.id, '%s {%s}' % (species.name, species.code)))
    #     return result


class AnimalSpecies_2(models.Model):
    _inherit = 'myo.animal.species'

    breed_ids = fields.One2many(
        'myo.animal',
        'species_id',
        'Breeds'
    )
    animal_ids = fields.One2many(
        'myo.animal',
        'species_id',
        'Animals'
    )
