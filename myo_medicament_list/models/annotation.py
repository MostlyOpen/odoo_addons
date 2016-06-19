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


class MedicamentList(models.Model):
    _inherit = 'myo.medicament.list'

    annotation_ids = fields.Many2many(
        'myo.annotation',
        'myo_medicament_list_annotation_rel',
        'medicament_list_id',
        'annotation_id',
        'Annotations'
    )


class Annotation(models.Model):
    _inherit = 'myo.annotation'

    medicament_list_ids = fields.Many2many(
        'myo.medicament.list',
        'myo_medicament_list_annotation_rel',
        'annotation_list_id',
        'medicament_id',
        'Medicament Lists'
    )


class MedicamentListVersion(models.Model):
    _inherit = 'myo.medicament.list.version'

    annotation_ids = fields.Many2many(
        'myo.annotation',
        'myo_medicament_list_version_annotation_rel',
        'medicament_list_version_id',
        'annotation_id',
        'Annotations'
    )


class Annotation_2(models.Model):
    _inherit = 'myo.annotation'

    medicament_list_version_ids = fields.Many2many(
        'myo.medicament.list.version',
        'myo_medicament_list_version_annotation_rel',
        'annotation_id',
        'medicament_list_version_id',
        'Medicament List Versions'
    )
