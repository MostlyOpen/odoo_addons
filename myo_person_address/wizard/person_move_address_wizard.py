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

import logging

_logger = logging.getLogger(__name__)


class PersonMoveAddressWizard(models.TransientModel):
    _name = 'myo.person.move_address.wizard'

    person_ids = fields.Many2many('myo.person', string='Persons')

    old_address_sign_out_date = fields.Date("Old Address Sign Out date",
                                            default=lambda *a: datetime.now().strftime('%Y-%m-%d'))

    new_address_id = fields.Many2one('myo.address', string='New Address')
    new_addres_sign_in_date = fields.Date('New Address Sign in date',
                                          default=lambda *a: datetime.now().strftime('%Y-%m-%d'))

    @api.multi
    def do_active_update(self):
        self.ensure_one()

        person_address_model = self.env['myo.person.address']

        for person_reg in self.person_ids:

            person_id = person_reg.id
            old_address_id = person_reg.address_id.id

            # print '>>>>>', user_id, person_id, old_address_id

            person_reg.address_id = self.new_address_id

            for person_address_reg in person_reg.person_address_ids:

                if person_address_reg.address_id.id == old_address_id and \
                   person_address_reg.sign_out_date is False:

                    # print '>>>>>>>>>>', person_address_reg.address_id.id, person_address_reg.sign_out_date

                    person_address_reg.sign_out_date = self.old_address_sign_out_date

                    values = {
                        'person_id': person_id,
                        'address_id': self.new_address_id.id,
                        'addres_sign_in_date': self.new_addres_sign_in_date,
                    }
                    person_address_model.create(values)

        return True

    @api.multi
    def do_reopen_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,  # this model
            'res_id': self.id,  # the current wizard record
            'view_type': 'form',
            'view_mode': 'form, tree',
            'target': 'new'}

    @api.multi
    def do_populate_marked_persons(self):
        self.ensure_one()
        self.person_ids = self._context.get('active_ids')
        # reopen wizard form on same wizard record
        return self.do_reopen_form()
