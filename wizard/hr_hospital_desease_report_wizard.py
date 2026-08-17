from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, time


class HrHospitalDeseaseReportWizard(models.TransientModel):
    """Wizard model for generating filtered disease report visits.

    Allows users to specify date ranges, target doctors, and diseases to filter
    and view matching hospital visit records grouped by disease.
    """

    _name = "hr.hospital.desease.report.wizard"
    _description = "Desease report"

    doctor_ids = fields.Many2many(
        comodel_name="hr.hospital.doctor",
    )
    desease_ids = fields.Many2many(comodel_name="hr.hospital.desease")
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        """Validate that the starting date does not exceed the ending date.

        Raises:
            ValidationError: If date_from is strictly after date_to.
        """

        for wizard in self:
            if (
                wizard.date_from
                and wizard.date_to
                and wizard.date_from > wizard.date_to
            ):
                raise ValidationError('"Date From" cannot be later than "Date To".')

    def action_generate_report(self):
        """Generate a filtered list view action of visit records based on wizard criteria.

        Converts date boundaries to full datetime bounds and applies doctor/disease domain filters.

        Returns:
            dict: An ir.actions.act_window action targeting hr.hospital.visit grouped by disease.
        """
        self.ensure_one()
        datetime_from = datetime.combine(self.date_from, time.min)
        datetime_to = datetime.combine(self.date_to, time.max)

        domain = [
            ("visit_datetime", ">=", datetime_from),
            ("visit_datetime", "<=", datetime_to),
        ]

        if self.doctor_ids:
            domain.append(("doctor_id", "in", self.doctor_ids.ids))
        if self.desease_ids:
            domain.append(("desease_id", "in", self.desease_ids.ids))

        return {
            "name": "Desease report",
            "type": "ir.actions.act_window",
            "res_model": "hr.hospital.visit",
            "view_mode": "list,form",
            "domain": domain,
            "context": {
                "group_by": ["desease_id"],
            },
            "target": "current",
        }
