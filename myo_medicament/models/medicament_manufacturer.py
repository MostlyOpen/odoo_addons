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

from openerp.osv import fields, osv


class MedicamentManufacturer_str(osv.osv):
    _name = 'myo.medicament.manufacturer.str'

    _columns = {
        'name': fields.char(string='Manufacturer String', required=True),
        'manufacturer_id': fields.many2one('myo.medicament.manufacturer', string='Associated Manufacturer',
                                           help='Associated Medicament Manufacturer'),
        'verify': fields.boolean('Verify'),
    }

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'Error! The Manufacturer String must be unique!'),
    ]

    _order = 'name'


class MedicamentManufacturer(osv.osv):
    _name = 'myo.medicament.manufacturer'

    def get_strings(self, cr, uid, ids, fields, arg, context):
        res = {}
        for record in self.browse(cr, uid, ids, context=None):
            strings = ''
            for str_id in record.str_ids:
                if strings == '':
                    strings = str_id.name
                else:
                    strings = strings + '\n' + str_id.name
            res[record.id] = strings
        return res

    _columns = {
        'name': fields.char(string='Manufacturer', required=True),
        'code': fields.char(string='Code'),
        'info': fields.text(string='Info'),
        'active': fields.boolean('Active',
                                 help="The active field allows you to hide the active component without removing it."),
        'str_ids': fields.one2many('myo.medicament.manufacturer.str', 'manufacturer_id', 'Strings'),
        'strings': fields.function(get_strings, method=True, string="Strings", type='char', store=False)
    }

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'Error! The Manufacturer must be unique!'),
        ('code_uniq', 'UNIQUE(code)', u'Error! The Code must be unique!'),
    ]

    _order = 'name'

    _defaults = {
        'active': 1,
    }


class MedicamentManufacturer_2(osv.osv):
    _inherit = 'myo.medicament.manufacturer'

    _columns = {
        'medicament_ids': fields.one2many('myo.medicament', 'manufacturer', 'Medicaments'),
    }
