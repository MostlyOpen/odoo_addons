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


class MedicamentActiveComponent_str(osv.osv):
    _name = 'myo.medicament.active_component.str'

    _columns = {
        'name': fields.char(sstring='Active Component String', required=True),
        'active_component_id': fields.many2one('myo.medicament.active_component', string='Associated Active Component',
                                               help='Associated Medicament Active Component'),
        'verify': fields.boolean('Verify'),
    }

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'Error! The Active Component String must be unique!'),
    ]

    _order = 'name'


class MedicamentActiveComponent(osv.osv):
    _name = 'myo.medicament.active_component'

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

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = name + ' {' + record['code'] + '}'
            res.append((record['id'], name))
        return res

    _columns = {
        'name': fields.char(sstring='Active Component', required=True),
        'code': fields.char(string='Code'),
        'info': fields.text(string='Info'),
        'active': fields.boolean('Active',
                                 help="The active field allows you to hide the active component without removing it."),
        'str_ids': fields.one2many('myo.medicament.active_component.str', 'active_component_id', 'Strings'),
        'strings': fields.function(get_strings, method=True, string="Strings", type='char', store=False)
    }

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'Error! The Active Component must be unique!'),
        ('code_uniq', 'UNIQUE(code)', u'Error! The Code must be unique!'),
    ]

    _order = 'name'

    _defaults = {
        'active': 1,
    }


class MedicamentActiveComponent_2(osv.osv):
    _inherit = 'myo.medicament.active_component'

    _columns = {
        'medicament_ids': fields.one2many('myo.medicament', 'active_component', 'Medicaments'),
    }
