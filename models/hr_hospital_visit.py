from odoo import models, fields


class HrHospitalVisit(models.Model):
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
        self.ensure_one()
        return {
            "name": "Visits with same desease",
            "type": "ir.actions.act_window",
            "res_model": "hr.hospital.visit",
            "view_mode": "list,form",
            "domain": [("desease_id", "=", self.desease_id.id)],
        }

    def write(self, vals):
        restricted_fields = {"doctor_id", "visit_datetime"}

        if self.visit_datetime:
            if restricted_fields.intersection(vals):
                raise Exception("You can't change visit datetime or doctor")

        return super().write(vals)

    def unlink(self):
        if self.visit_datetime:
            raise Exception(
                "It is not possible to delete a visit that has already taken place."
            )
