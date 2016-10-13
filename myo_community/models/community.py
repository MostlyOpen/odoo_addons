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


class Community(models.Model):
    _name = "myo.community"

    name = fields.Char('Community', required=True, translate=False)
    alias = fields.Char('Alias', help='Common name that the Community is referred')
    parent_id = fields.Many2one(
        'myo.community',
        'Parent Community',
        index=True,
        ondelete='restrict'
    )
    code = fields.Char(size=64, string='Community Code', required=False)
    comm_location = fields.Char('Community Location')
    notes = fields.Text(string='Notes')
    complete_name = fields.Char(
        string='Full Category',
        compute='_name_get_fnc',
        store=False,
        readonly=True
    )
    child_ids = fields.One2many('myo.community', 'parent_id', 'Child Communities')
    date_inclusion = fields.Datetime(
        "Inclusion Date",
        required=False,
        readonly=False,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    user_id = fields.Many2one('res.users', 'Community Responsible')
    active = fields.Boolean(
        'Active',
        help="If unchecked, it will allow you to hide the community without removing it.",
        default=True
    )
    parent_left = fields.Integer('Left parent', index=True)
    parent_right = fields.Integer('Right parent', index=True)

    _sql_constraints = [
        (
            'code_uniq',
            'UNIQUE (code)',
            'Error! The Code must be unique!'
        ),
    ]

    _constraints = [
        (
            models.Model._check_recursion,
            'Error! You can not create recursive communities.',
            ['parent_id']
        ),
    ]

    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    @api.multi
    def name_get(self):
        """Return the community's display name, including their direct
           parent by default.

        :param dict context: the ``community_display`` key can be
                             used to select the short version of the
                             community (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if self._context is None:
            self._context = {}
        if self._context.get('community_display') == 'short':
            return super(Community, self).name_get()
        if isinstance(self._ids, (int, long)):
            self._ids = [self._ids]
        reads = self.read(['name', 'parent_id'])
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        communities = self.search(args, limit=limit)
        return communities.name_get()

    @api.one
    def _name_get_fnc(self):
        self.refresh_complete_name = 0
        complete_name = self.name_get()
        if complete_name:
            self.complete_name = complete_name[0][1]
        else:
            self.complete_name = self.name
