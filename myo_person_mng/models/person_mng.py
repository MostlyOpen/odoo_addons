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
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models


class PersonManagement(models.Model):
    _name = 'myo.person.mng'

    name = fields.Char('Name', required=True)
    alias = fields.Char('Alias', help='Common name that the Person is referred.')
    code = fields.Char(string='Person Code', required=False)
    notes = fields.Text(string='Notes')
    date_inclusion = fields.Datetime("Inclusion Date", required=False, readonly=False,
                                     default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    batch_name = fields.Char('Batch Name', required=False)
    country_id_2 = fields.Many2one('res.country', 'Nationality')
    birthday = fields.Date("Date of Birth")
    age = fields.Char(
        string='Age',
        compute='_compute_age',
        store=True
    )
    spouse_name = fields.Char('Spouse Name')
    spouse_id = fields.Many2one('myo.person', 'Spouse', ondelete='restrict')
    father_name = fields.Char('Father Name')
    father_id = fields.Many2one('myo.person', 'Father', ondelete='restrict')
    mother_name = fields.Char('Mother Name')
    mother_id = fields.Many2one('myo.person', 'Mother', ondelete='restrict')
    responsible_name = fields.Char('Responsible Name')
    responsible_id = fields.Many2one('myo.person', 'Responsible', ondelete='restrict')
    identification_id = fields.Char('Person ID')
    otherid = fields.Char('Other ID')
    gender = fields.Selection(
        [('M', 'Male'),
         ('F', 'Female')
         ], 'Gender'
    )
    marital = fields.Selection(
        [('single', 'Single'),
         ('married', 'Married'),
         ('widower', 'Widower'),
         ('divorced', 'Divorced'),
         ], 'Marital Status'
    )
    active = fields.Boolean('Active',
                            help="If unchecked, it will allow you to hide the person without removing it.",
                            default=1)
    person_id = fields.Many2one('myo.person', 'Person')

    _order = 'name'

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE(code)',
         u'Error! The Person Code must be unique!'
         )
    ]

    @api.multi
    @api.constrains('birthday')
    def _check_birthday(self):
        for person in self:
            if person.birthday > fields.Date.today():
                raise Warning(u'Error! Date of Birth must be in the past!')

    @api.one
    @api.depends('birthday')
    def _compute_age(self):
        now = datetime.now()
        if self.birthday:
            dob = datetime.strptime(self.birthday, '%Y-%m-%d')
            delta = relativedelta(now, dob)
            # self.age = str(delta.years) + "y " + str(delta.months) + "m " + str(delta.days) + "d"
            self.age = str(delta.years)
        else:
            self.age = "No Date of Birth!"
