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

from openerp import fields, models


class Tag(models.Model):
    _inherit = 'myo.tag'

    insurance_plan_ids = fields.Many2many(
        'myo.insurance.plan',
        'myo_insurance_plan_tag_rel',
        'tag_id',
        'insurance_plan_id',
        'Insurance Plans'
    )


class InsurancePlan(models.Model):
    _inherit = 'myo.insurance.plan'

    tag_ids = fields.Many2many(
        'myo.tag',
        'myo_insurance_plan_tag_rel',
        'insurance_plan_id',
        'tag_id',
        'Tags'
    )
