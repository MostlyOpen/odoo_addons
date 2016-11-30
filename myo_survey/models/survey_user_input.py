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


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    active = fields.Boolean(
        'Active',
        help="If unchecked, it will allow you to hide the survey user input without removing it.",
        default=1
    )
    link_survey_user_input = fields.Boolean(
        'Link Survey User Input',
        help="",
        default=0
    )
    linked_code = fields.Char('Linked Code', help="Linked Code")
    linked_message = fields.Char('Linked Message', help="Linked Message")
    linked_state = fields.Selection(
        [('draft', 'Draft'),
         ('revised', 'Revised'),
         ('waiting', 'Waiting'),
         ('linked', 'Linked'),
         ('canceled', 'Canceled')
         ], string='Linkded Status', default='draft', readonly=False, required=False, help=""
    )

    @api.multi
    def write(self, values):
        if 'link_survey_user_input' in values:
            del values['link_survey_user_input']

            for survey_user_input in self:
                if survey_user_input.linked_state == 'draft':
                    if len(survey_user_input.user_input_line_ids) > 0:
                        linked_code = survey_user_input.user_input_line_ids[0].value_text
                        values['linked_code'] = linked_code
                        values['linked_state'] = 'revised'
                        document_model = self.env['myo.document']
                        document = document_model.search([('code', '=', linked_code), ])
                        if document.id != []:
                            document.survey_user_input_id = survey_user_input.id
                            document.state = 'done'
                            values['linked_state'] = 'linked'
                    super(SurveyUserInput, survey_user_input).write(values)
            return True

        else:
            return super(SurveyUserInput, self).write(values)
