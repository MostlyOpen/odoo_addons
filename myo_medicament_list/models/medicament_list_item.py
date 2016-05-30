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


class MedicamentListItem(models.Model):
    _name = 'myo.medicament.list.item'

    list_version_id = fields.Many2one('myo.medicament.list.version', string='Medicament List Version',
                                      help='Medicament List Version', required=False)
    medicament_id = fields.Many2one('myo.medicament', string='Medicament',
                                    help='Medicament', required=False)
    medicament_ref = fields.Reference([('myo.medicament', 'Medicament'),
                                       ], 'Medicament Reference')
    notes = fields.Text(string='Notes')
    order = fields.Integer(string='Order', default=10)
    active = fields.Boolean('Active',
                            help='The active field allows you to hide the medicament list item without removing it.',
                            default=1)

    _order = 'list_version_id, order'


class MedicamentListVersion(models.Model):
    _inherit = 'myo.medicament.list.version'

    medicament_list_item_ids = fields.One2many(
        'myo.medicament.list.item',
        'list_version_id',
        'Medicament List Itens'
    )
    count_items = fields.Integer(
        'Number of Items',
        compute='_compute_count_items'
    )

    @api.depends('medicament_list_item_ids')
    def _compute_count_items(self):
        for r in self:
            r.count_items = len(r.medicament_list_item_ids)
