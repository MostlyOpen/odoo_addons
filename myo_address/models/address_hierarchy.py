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


class Address(models.Model):
    _inherit = 'myo.address'

    parent_id = fields.Many2one(
        'myo.address',
        'Parent Address',
        index=True,
        ondelete='restrict'
    )
    complete_name = fields.Char(
        string='Complete Name',
        compute='_name_get_fnc',
        store=False,
        readonly=True
    )
    child_ids = fields.One2many('myo.address', 'parent_id', 'Child Addresses')
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)

    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    _constraints = [
        (
            models.Model._check_recursion,
            'Error! You can not create recursive addresses.',
            ['parent_id']
        ),
    ]

    @api.multi
    def name_get_(self):
        """Return the address's display name, including their direct parent by default.

        :param dict context: the ``address_display`` key can be
                             used to select the short version of the
                             address (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if self._context is None:
            self._context = {}
        if self._context.get('address_display') == 'short':
            return super(Address, self).name_get()
        if isinstance(self._ids, (int, long)):
            self._ids = [self._ids]
        reads = self.read(['name', 'parent_id'])
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = self.parent_id.name_get_()[0][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    # @api.model
    # def name_search(self, name, args=None, operator='ilike', limit=100):
    #     args = args or []
    #     if name:
    #         # Be sure name_search is symetric to name_get
    #         name = name.split(' / ')[-1]
    #         args = [('name', operator, name)] + args
    #     addresss = self.search(args, limit=limit)
    #     return addresss.name_get()

    @api.one
    def _name_get_fnc(self):
        self.refresh_complete_name = 0
        complete_name = self.name_get_()
        if complete_name:
            self.complete_name = complete_name[0][1]
        else:
            self.complete_name = self.name
