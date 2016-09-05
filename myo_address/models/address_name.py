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

    name = fields.Char(string="Name", required=True, default=False,
                       help='Use "/" to get an automatic new Address Name.')
    suggested_name = fields.Char(string="Suggested Name", required=False, store=True,
                                 compute="_get_suggested_name",
                                 help='Suggested Name for the Address.')
    automatic_set_name = fields.Boolean(
        'Automatic Name',
        help="If checked, the Address Name will be set automatically.",
        default=True
    )

    @api.depends('street', 'street2')
    def _get_suggested_name(self):
        if self.street:
            self.suggested_name = self.street
            if self.street2:
                self.suggested_name = self.suggested_name + ' - ' + self.street2
        else:
            if not self.suggested_name:
                if self.code:
                    self.suggested_name = self.code

    @api.multi
    def write(self, values):
        ret = super(Address, self).write(values)
        if self.automatic_set_name:
            if self.name != self.suggested_name:
                values['name'] = self.suggested_name
                return super(Address, self).write(values)
        else:
            if ('name' in values and values['name'] == '/') or \
               (self.name == '/'):
                values['name'] = self.suggested_name
                return super(Address, self).write(values)
        return ret
