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


class AnimalBreed(models.Model):
    _name = 'myo.animal.breed'

    name = fields.Char(string='Breed', required=True)
    code = fields.Char(string='Code')
    species_id = fields.Many2one('myo.animal.species', 'Species', ondelete='restrict')
    notes = fields.Text(string='Notes')
    active = fields.Boolean('Active',
                            help="The active field allows you to hide the breed without removing it.",
                            default=1)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'Error! The Breed must be unique!'),
        ('code_uniq', 'UNIQUE(code)', u'Error! The Code must be unique!'),
    ]

    _order = 'name'

    # @api.multi
    # @api.depends('name', 'code')
    # def name_get(self):
    #     result = []
    #     for breed in self:
    #         result.append((breed.id, '%s {%s}' % (breed.name, breed.code)))
    #     return result


class AnimalBreed_2(models.Model):
    _inherit = 'myo.animal.breed'

    animal_ids = fields.One2many(
        'myo.animal',
        'breed_id',
        'Animals'
    )
