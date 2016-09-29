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


class InsuredCategory(models.Model):
    _name = 'myo.insured.category'

    name = fields.Char('Category', required=True, translate=True)
    parent_id = fields.Many2one(
        'myo.insured.category',
        'Parent Category',
        index=True,
        ondelete='restrict'
    )
    code = fields.Char('Code', required=False)
    description = fields.Char(string='Description')
    notes = fields.Text(string='Notes')
    complete_name = fields.Char(
        string='Full Category',
        compute='_name_get_fnc',
        store=False,
        readonly=True
    )
    child_ids = fields.One2many('myo.insured.category', 'parent_id', 'Child Categories')
    active = fields.Boolean(
        'Active',
        help="If unchecked, it will allow you to hide the category without removing it.",
        default=True
    )
    parent_left = fields.Integer('Left parent', index=True)
    parent_right = fields.Integer('Right parent', index=True)
    insured_ids = fields.Many2many(
        'myo.insured',
        'myo_insured_category_rel',
        'category_id',
        'insured_id',
        'Insureds'
    )

    _sql_constraints = [
        (
            'uniq_code',
            'UNIQUE(code)',
            'Error! The Code must be unique!'
        ),
    ]

    _constraints = [
        (
            models.Model._check_recursion,
            'Error! You can not create recursive categories.',
            ['parent_id']
        ),
    ]

    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    @api.multi
    def name_get(self):
        """Return the category's display name, including their direct parent by default.

        :param dict context: the ``category_display`` key can be
                             used to select the short version of the
                             category (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if self._context is None:
            self._context = {}
        if self._context.get('category_display') == 'short':
            return super(InsuredCategory, self).name_get()
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
        categories = self.search(args, limit=limit)
        return categories.name_get()

    @api.one
    def _name_get_fnc(self):
        self.refresh_complete_name = 0
        complete_name = self.name_get()
        if complete_name:
            self.complete_name = complete_name[0][1]
        else:
            self.complete_name = self.name


class Insured(models.Model):
    _inherit = 'myo.insured'

    category_ids = fields.Many2many(
        'myo.insured.category',
        'myo_insured_category_rel',
        'insured_id',
        'category_id',
        'Categories'
    )
