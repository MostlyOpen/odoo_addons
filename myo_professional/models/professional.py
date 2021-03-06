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


class Professional(models.Model):
    _name = 'myo.professional'

    name = fields.Char('Name', required=True)
    alias = fields.Char('Alias', help='Common name that the Professional is referred')
    code = fields.Char(string='Code', help='Professional Code', required=False)
    user_id = fields.Many2one('res.users', 'Related User', required=False, readonly=False)
    notes = fields.Text(string='Notes')
    date_inclusion = fields.Datetime("Inclusion Date", required=False, readonly=False,
                                     default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    active = fields.Boolean('Active',
                            help="If unchecked, it will allow you to hide the professional without removing it.",
                            default=1)
    professional_id = fields.Char(size=64, string='Professional ID', required=False)

    _order = 'name'

    _sql_constraints = [
        ('professional_code_uniq', 'unique(code)', u'Error! The Professional Code must be unique!'),
        ('professional_id_uniq', 'unique(professional_id)', u'Error! The Professional ID must be unique!'),
    ]

    @api.multi
    @api.depends('name', 'professional_id')
    def name_get(self):
        result = []
        for myo_professional in self:
            if myo_professional.professional_id is not False:
                result.append((myo_professional.id, '%s [%s]' %
                              (myo_professional.name, myo_professional.professional_id)))
            else:
                result.append((myo_professional.id, '%s' % (myo_professional.name)))
        return result
