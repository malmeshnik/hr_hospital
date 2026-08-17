from odoo import models, fields


class HrHospitalVisit(models.Model):
    """Model representing a medical appointment or visit.

    Tracks visit statuses, scheduling, linked patient, doctor, and diagnosed
    disease details, while enforcing immutability on completed visit records.
    """
    _name = "hr.hospital.visit"
    _description = "Visit"

    status = fields.Selection(
        selection=[
            ("planned", "Planned"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ]
    )

    scheduled_datetime = fields.Datetime()

    patient_id = fields.Many2one("hr.hospital.patient", string="Patient")
    doctor_id = fields.Many2one("hr.hospital.doctor", string="Doctor")
    desease_id = fields.Many2one("hr.hospital.desease", string="Desease")

    visit_datetime = fields.Datetime(default=fields.Datetime.now)

    summary = fields.Html()

    def action_view_same_desease_visits(self):
        """Return an action displaying all visits associated with the same disease.

        Returns:
            dict: An ir.actions.act_window action dictionary filtered by desease_id.
        """

        self.ensure_one()
        return {
            "name": "Visits with same desease",
            "type": "ir.actions.act_window",
            "res_model": "hr.hospital.visit",
            "view_mode": "list,form",
            "domain": [("desease_id", "=", self.desease_id.id)],
        }

    def write(self, vals):
        """Override write to prevent modifying critical fields once a visit datetime is set.

        Args:
            vals (dict): Dictionary of field values to update.

        Raises:
            Exception: If restricted fields (doctor_id, visit_datetime) are modified on an existing visit.
        """

        restricted_fields = {"doctor_id", "visit_datetime"}

        if self.visit_datetime:
            if restricted_fields.intersection(vals):
                raise Exception("You can't change visit datetime or doctor")

        return super().write(vals)

    def unlink(self):
        """Override unlink to prevent deletion of completed or held visits.

        Raises:
            Exception: If attempting to delete a visit record that has a visit_datetime set.
        """
        
        if self.visit_datetime:
            raise Exception(
                "It is not possible to delete a visit that has already taken place."
            )
