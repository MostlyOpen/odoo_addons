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


class DocumentLog(models.Model):
    _name = 'myo.document.log'

    document_id = fields.Many2one('myo.document', 'Document', required=True, ondelete='cascade')
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


class Document(models.Model):
    _inherit = 'myo.document'

    log_ids = fields.One2many('myo.document.log', 'document_id', 'Document Log',
                              readonly=True)
    active_log = fields.Boolean(
        'Active Log',
        help="If unchecked, it will allow you to disable the log without removing it.",
        default=True
    )

    @api.one
    def insert_myo_document_log(self, document_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            vals = {
                'document_id': document_id,
                'values': values,
                'action': action,
                'notes': notes,
            }
            self.pool.get('myo.document.log').create(self._cr, self._uid, vals)

    @api.multi
    def write(self, values):
        action = 'write'
        notes = False
        for document in self:
            document.insert_myo_document_log(document.id, values, action, notes)
        return super(Document, self).write(values)

    @api.model
    def create(self, values):
        action = 'create'
        notes = False
        record = super(Document, self).create(values)
        record.insert_myo_document_log(record.id, values, action, notes)
        return record
