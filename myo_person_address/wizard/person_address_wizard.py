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


class PersonAddressWizard(models.TransientModel):
    _name = 'myo.person.address.wizard'

    person_address_ids = fields.Many2many('myo.person.address', string='Person Addresses')
    new_active = fields.Boolean('Set Active', default=True)

    @api.multi
    def do_mass_update(self):
        self.ensure_one()
        _logger.debug('Mass update on Person Addresses %s',
                      self.person_address_ids.ids)
        self.person_address_ids.write({'active': self.new_active})
        domain = [('active', '=', False), ]
        inactive_recs = self.person_address_ids.search(domain)
        inactive_recs.write({'active': self.new_active})
        return True

    @api.multi
    def do_count_person_addresss(self):
        PersonAddress = self.env['myo.person.address']
        count = PersonAddress.search_count([])
        domain = [('active', '=', False), ]
        count_inactive = PersonAddress.search_count(domain)
        raise exceptions.Warning(
            'There are %d active and %d inactive person addresses.' % (count, count_inactive)
        )

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
    def do_populate_person_addresss(self):
        self.ensure_one()
        PersonAddress = self.env['myo.person.address']
        all_person_addresss = PersonAddress.search([])
        self.person_address_ids = all_person_addresss
        # reopen wizard form on same wizard record
        return self.do_reopen_form()
