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


def format_name(name_seq):
    name = map(int, str(name_seq))
    name_len = len(name)
    while len(name) < 14:
        name.insert(0, 0)
    while len(name) < 16:
        n = sum([(len(name) + 1 - i) * v for i, v in enumerate(name)]) % 11
        if n > 1:
            f = 11 - n
        else:
            f = 0
        name.append(f)
    name_str = "%s.%s.%s.%s.%s-%s" % (str(name[0]) + str(name[1]),
                                      str(name[2]) + str(name[3]) + str(name[4]),
                                      str(name[5]) + str(name[6]) + str(name[7]),
                                      str(name[8]) + str(name[9]) + str(name[10]),
                                      str(name[11]) + str(name[12]) + str(name[13]),
                                      str(name[14]) + str(name[15]))
    if name_len <= 3:
        name_form = name_str[18 - name_len:21]
    elif name_len > 3 and name_len <= 6:
        name_form = name_str[17 - name_len:21]
    elif name_len > 6 and name_len <= 9:
        name_form = name_str[16 - name_len:21]
    elif name_len > 9 and name_len <= 12:
        name_form = name_str[15 - name_len:21]
    elif name_len > 12 and name_len <= 14:
        name_form = name_str[14 - name_len:21]
    return name_form


class Document(models.Model):
    _inherit = 'myo.document'

    name = fields.Char(string='Code', required=False, default=False,
                       help='Use "/" to get an automatic new Document Code.')

    @api.model
    def create(self, values):
        if 'name' not in values or ('name' in values and values['name'] == '/'):
            name_seq = self.pool.get('ir.sequence').next_by_code(self._cr, self._uid, 'myo.document.code')
            values['name'] = format_name(name_seq)
        return super(Document, self).create(values)

    @api.multi
    def write(self, values):
        if 'name' in values and values['name'] == '/':
            name_seq = self.pool.get('ir.sequence').next_by_code(self._cr, self._uid, 'myo.document.code')
            values['name'] = format_name(name_seq)
        return super(Document, self).write(values)

    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        default.update({'name': '/', })
        return super(Document, self).copy(default)
