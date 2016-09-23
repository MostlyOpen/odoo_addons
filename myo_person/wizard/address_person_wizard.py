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

from openerp import exceptions

import logging

_logger = logging.getLogger(__name__)


class AddressPersonWizard(models.TransientModel):
    _name = 'myo.address.person.wizard'

    address_person_ids = fields.Many2many('myo.address.person', string='Address Persons')
    new_active = fields.Boolean('Set Active', default=True)

    @api.multi
    def do_mass_update(self):
        self.ensure_one()
        _logger.debug('Mass update on Address Persons %s',
                      self.address_person_ids.ids)
        self.address_person_ids.write({'active': self.new_active})
        domain = [('active', '=', False), ]
        inactive_recs = self.address_person_ids.search(domain)
        inactive_recs.write({'active': self.new_active})
        return True

    @api.multi
    def do_count_address_persons(self):
        AddressPerson = self.env['myo.address.person']
        count = AddressPerson.search_count([])
        raise exceptions.Warning(
            'There are %d active addresse persons.' % count)

    @api.multi
    def do_reopen_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,  # this model
            'res_id': self.id,  # the current wizard record
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}

    @api.multi
    def do_populate_address_persons(self):
        self.ensure_one()
        AddressPerson = self.env['myo.address.person']
        all_address_persons = AddressPerson.search([])
        self.address_person_ids = all_address_persons
        # reopen wizard form on same wizard record
        return self.do_reopen_form()
