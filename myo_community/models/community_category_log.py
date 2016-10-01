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

from datetime import *


class CommunityCategoryLog(models.Model):
    _name = 'myo.community.category.log'

    community_category_id = fields.Many2one(
        'myo.community.category',
        'Community Category',
        required=True,
        ondelete='cascade'
    )
    user_id = fields.Many2one(
        'res.users',
        'User',
        required=True,
        default=lambda self: self.env.user
    )
    date_log = fields.Datetime(
        'When',
        required=True,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    values = fields.Text(string='Values')
    action = fields.Char(string='Action')
    notes = fields.Text(string='Notes')

    _order = "date_log desc"


class CommunityCategory(models.Model):
    _inherit = 'myo.community.category'

    log_ids = fields.One2many('myo.community.category.log', 'community_category_id', 'Community Category Log',
                              readonly=True)
    active_log = fields.Boolean(
        'Active Log',
        help="If unchecked, it will allow you to disable the log without removing it.",
        default=True
    )

    @api.one
    def insert_myo_community_category_log(self, community_category_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            vals = {
                'community_category_id': community_category_id,
                'values': values,
                'action': action,
                'notes': notes,
            }
            self.pool.get('myo.community.category.log').create(self._cr, self._uid, vals)

    @api.multi
    def write(self, values):
        action = 'write'
        notes = False
        for community_category in self:
            community_category.insert_myo_community_category_log(community_category.id, values, action, notes)
        return super(CommunityCategory, self).write(values)

    @api.model
    def create(self, values):
        action = 'create'
        notes = False
        record = super(CommunityCategory, self).create(values)
        record.insert_myo_community_category_log(record.id, values, action, notes)
        return record
