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

from openerp import api, fields, models


class MedicamentListVersion(models.Model):
    _name = 'myo.medicament.list.version'

    list_id = fields.Many2one('myo.medicament.list', 'Medicament List')
    name = fields.Char('List Version', required=True)
    code = fields.Char('List Version Code', required=False)
    description = fields.Char(string='Description')
    date_inclusion = fields.Datetime("Inclusion Date", required=False, readonly=False,
                                     default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    notes = fields.Text(string='Notes')
    active = fields.Boolean('Active',
                            help='The active field allows you to hide the list version without removing it.',
                            default=1)

    _sql_constraints = [
        ('uniq_list_code', 'unique(code)', "Error! The List Version Code must be unique!"),
    ]

    @api.multi
    def name_get(self):
        """Return the version's display name, including their direct list by default.

        :param dict context: the ``list_version_display`` key can be
                             used to select the short version of the
                             version (without the direct list),
                             when set to ``'short'``. The default is
                             the long version."""
        if self._context is None:
            self._context = {}
        if self._context.get('list_version_display') == 'short':
            return super(MedicamentListVersion, self).name_get()
        if isinstance(self._ids, (int, long)):
            self._ids = [self._ids]
        reads = self.read(['name', 'list_id'])
        res = []
        for record in reads:
            name = record['name']
            if record['list_id']:
                name = record['list_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res


class MedicamentList(models.Model):
    _inherit = 'myo.medicament.list'

    current_version_id = fields.Many2one(
        'myo.medicament.list.version',
        'Current List Version',
        domain="[('list_id','=',id)]"
    )
    medicament_list_version_ids = fields.One2many(
        'myo.medicament.list.version',
        'list_id',
        'Medicament List Versions'
    )
