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

from datetime import *

from openerp import api, fields, models


class MediaFile(models.Model):
    _name = 'myo.mfile'

    name = fields.Char('Name', required=True, translate=False)
    alias = fields.Char('Alias', help='Common name that the file is referred')
    code = fields.Char(string='Code', required=False)
    path = fields.Char(string='Path', compute='_compute_path_str', store=False, readonly=True)
    description_old = fields.Text(string='Description', translate=False)
    description = fields.Html(string='Description', translate=False)
    notes_old = fields.Text(string='Notes')
    notes = fields.Html(string='Notes', translate=False)
    date_inclusion = fields.Datetime('Inclusion Date',
                                     default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    active = fields.Boolean('Active',
                            help="If unchecked, it will allow you to hide the media file without removing it.",
                            default=1)
    url = fields.Char('URL', help="URL of the File")
    parent_id = fields.Many2one('myo.mfile', 'Parent File')
    child_ids = fields.One2many('myo.mfile', 'parent_id', 'Child Files')

    _order = 'name'

    _sql_constraints = [('code_uniq', 'unique(code)', u'Error! The Code must be unique!')]

    @api.one
    def _compute_path_str(self):
        if self.code:
            if self.alias:
                self.path = self.alias
            else:
                self.path = self.code
