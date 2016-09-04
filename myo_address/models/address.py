# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

from openerp import api
from openerp.osv import osv, fields

from lxml import etree

ADDRESS_FORMAT_CLASSES = {
    '%(city)s %(state_code)s\n%(zip)s': 'o_city_state',
    '%(zip)s %(city)s': 'o_zip_city'
}


class FormatAddress(object):
    @api.model
    def fields_view_get_address(self, arch):
        address_format = self.env.user.company_id.country_id.address_format or ''
        for format_pattern, format_class in ADDRESS_FORMAT_CLASSES.iteritems():
            if format_pattern in address_format:
                doc = etree.fromstring(arch)
                for address_node in doc.xpath("//div[@class='o_address_format']"):
                    # add address format class to address block
                    address_node.attrib['class'] += ' ' + format_class
                    if format_class.startswith('o_zip'):
                        zip_fields = address_node.xpath("//field[@name='zip']")
                        city_fields = address_node.xpath("//field[@name='city']")
                        if zip_fields and city_fields:
                            # move zip field before city field
                            city_fields[0].addprevious(zip_fields[0])
                arch = etree.tostring(doc)
                break
        return arch

ADDRESS_FIELDS = ('street', 'street2', 'zip', 'city', 'state_id', 'country_id')


class Address(osv.Model, FormatAddress):
    _name = "myo.address"

    _columns = {
        'name': fields.char('Name', required=True, select=True),
        'title': fields.many2one('res.partner.title', 'Title'),
        'alias': fields.char('Alias', help='Common name that the Address is referred.'),
        'code': fields.char(string='Code', required=False, help="Address Code"),
        'notes': fields.text('Notes'),
        'street': fields.char('Street'),
        'street2': fields.char('Street2'),
        'zip': fields.char('ZIP code', change_default=True),
        'city': fields.char('City'),
        'state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'email': fields.char('Email'),
        'phone': fields.char('Phone'),
        'fax': fields.char('Fax'),
        'mobile': fields.char('Mobile'),
        'active': fields.boolean('Active',
                                 help="If unchecked, it will allow you to hide the address without removing it."
                                 ),
    }

    _order = "name"

    def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        if (not view_id) and (view_type == 'form') and context and context.get('force_email', False):
            view_id = self.pool['ir.model.data'].get_object_reference(cr, user, 'base', 'view_address_simple_form')[1]
        res = super(Address, self).fields_view_get(cr, user, view_id, view_type, context,
                                                   toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            res['arch'] = self.fields_view_get_address(cr, user, res['arch'], context=context)
        return res

    _defaults = {
        'active': True,
    }

    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}

    def _address_fields(self, cr, uid, context=None):
        return list(ADDRESS_FIELDS)

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            if context.get('show_address_only'):
                name = self._display_address(cr, uid, record, context=context)
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, context=context)
            name = name.replace('\n\n', '\n')
            name = name.replace('\n\n', '\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            res.append((record.id, name))
        return res

    @api.model
    @api.returns('self')
    def main_address(self):
        ''' Return the main address '''
        return self.env.ref('base.main_address')

    def _display_address(self, cr, uid, address, context=None):

        '''
        The purpose of this function is to build and return an address formatted accordingly to the
        standards of the country where it belongs.

        :param address: browse record of the address to format
        :returns: the address formatted in a display that fit its country habits (or the default ones
            if not country is specified)
        :rtype: string
        '''

        # get the information that will be injected into the display format
        # get the address format
        address_format = address.country_id.address_format or \
            "%(street)s\n%(street2)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s"
        args = {
            'state_code': address.state_id.code or '',
            'state_name': address.state_id.name or '',
            'country_code': address.country_id.code or '',
            'country_name': address.country_id.name or '',
        }
        for field in self._address_fields(cr, uid, context=context):
            args[field] = getattr(address, field) or ''
        return address_format % args
