from odoo import models, fields


class HrHospitalPatient(models.Model):
    """Model representing a hospital patient.

    Inherits general medical attributes from hr.hospital.medic.info and manages
    personal identifiers, assigned attending doctor, historical assignments,
    and medical visits.
    """

    _name = "hr.hospital.patient"
    _description = "Patient"
    _inherit = "hr.hospital.medic.info"

    name = fields.Char()
    insurance_number = fields.Char(size=20)
    phone = fields.Char(size=25)

    system_user = fields.Many2many(comodel_name="res.users")
    doctor_id = fields.Many2one(comodel_name="hr.hospital.doctor")
    doctor_history_ids = fields.One2many(
        comodel_name="hr.hospital.doctor.history", inverse_name="patient_id"
    )
    visit_ids = fields.One2many(
        comodel_name="hr.hospital.visit", inverse_name="patient_id"
    )

    def action_view_patient_visits_history(self):
        """Return an action opening the list view of all visits for this patient.

        Returns:
            dict: An ir.actions.act_window action dictionary filtered by patient_id.
        """
        self.ensure_one()
        return {
            "name": "Patient visits history",
            "type": "ir.actions.act_window",
            "res_model": "hr.hospital.visit",
            "view_mode": "list,form",
            "domain": [("patient_id", "=", self.id)],
        }

    def action_create_visit(self):
        """Return a wizard action to create a new visit for this patient in a popup dialog.

        Returns:
            dict: An ir.actions.act_window target='new' action with default_patient_id set.
        """
        
        self.ensure_one()
        return {
            "name": "New visit",
            "type": "ir.actions.act_window",
            "res_model": "hr.hospital.visit",
            "view_mode": "form",
            "target": "new",
            "context": {"default_patient_id": self.id},
        }
