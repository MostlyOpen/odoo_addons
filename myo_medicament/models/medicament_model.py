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
import math

from openerp import fields, models


def ean_checksum(eancode):
    '''returns the checksum of an ean string of length 13, returns -1 if the string has the wrong length'''
    if len(eancode) != 13:
        return -1
    oddsum = 0
    evensum = 0
    total = 0
    eanvalue = eancode
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10
    return check


def check_ean(eancode):
    '''returns True if eancode is a valid ean13 string, or null'''
    if not eancode:
        return True
    if len(eancode) != 13:
        return False
    try:
        int(eancode)
    except:
        return False
    return ean_checksum(eancode) == int(eancode[-1])


class MedicamentModel(models.AbstractModel):
    _name = 'myo.medicament.model'

    name = fields.Char('Product Name', select=True, required=True)
    ean13 = fields.Char('EAN13 Barcode', size=13,
                        help="International Article Number used for product identification.")
    code = fields.Char(string='Medicament Code', required=False)
    medicament_name = fields.Char(string='Medicament Name')
    concentration = fields.Char(string='Concentration')
    presentation = fields.Char(string='Presentation')
    pres_form = fields.Many2one('myo.medicament.form', string='Presentation Form',
                                help='Medicament form, such as tablet or gel')
    pres_quantity = fields.Float(string='Presentation Quantity')
    pres_quantity_unit = fields.Many2one('myo.medicament.uom', string='Presentation Quantity Unit',
                                         help='Unit of measure for the medicament to be taken')
    notes = fields.Text(string='Notes')
    date_inclusion = fields.Datetime("Inclusion Date", required=False, readonly=False,
                                     default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    active = fields.Boolean('Active',
                            help="The active field allows you to hide the medicament without removing it.",
                            default=True)
    is_product = fields.Boolean('Is a Product',
                                help="Check if the medicament is a product.",
                                default=False)
    is_fraction = fields.Boolean('Is a Fraction',
                                 help="Check if the medicament is a fraction of a product.",
                                 default=False)
    for_hospital_use = fields.Boolean('For Hospital Use',
                                      help="Check if for hospital use only.",
                                      default=False)

    _order = 'name'

    _sql_constraints = [
        ('name_uniq', 'unique(name)', u'Error! The Medicament Name must be unique!'),
        ('code_uniq', 'unique(code)', u'Error! The Medicament Code must be unique!'),
    ]

    def _check_ean_key(self, cr, uid, ids, context=None):
        for medicament in self.read(cr, uid, ids, ['ean13'], context=context):
            if not check_ean(medicament['ean13']):
                return False
        return True

    _constraints = [(_check_ean_key,
                     'You provided an invalid "EAN13 Barcode" reference. ' +
                     'You may use the "Internal Reference" field instead.',
                     ['ean13'])]


class MedicamentModel_2(models.AbstractModel):
    _inherit = 'myo.medicament.model'

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

    def name_active_component_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'active_component_name'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['active_component_name']:
                name = name + ' (' + record['active_component_name'] + ')'
            res.append((record['id'], name))
        return res

    def _name_active_component_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_active_component_get(cr, uid, ids, context=context)
        return dict(res)

    active_component = fields.Many2one('myo.medicament.active_component',
                                       string='Active Component',
                                       help='Medicament Active Component')
    name_active_component = fields.Char('Name (Active Component)', compute='_name_active_component_get_fnc')
    active_component_name = fields.Char(related='active_component.name',
                                        string='Related Active Component')


class MedicamentModel_3(models.AbstractModel):
    _inherit = 'myo.medicament.model'

    manufacturer = fields.Many2one('myo.medicament.manufacturer',
                                   string='Manufacturer',
                                   help='Medicament Manufacturer')
    manufacturer_name = fields.Char(related='manufacturer.name',
                                    string='Related Manufacturer')
