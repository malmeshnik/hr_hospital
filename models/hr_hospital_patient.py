from odoo import models, fields


class HrHospitalPatient(models.Model):
    _name = "hr.hospital.patient"
    _description = "Patient"
    _inherit = "hr.hospital.medic.info"

    name = fields.Char()
    insurance_number = fields.Char(size=20)
    phone = fields.Char(size=25)

    doctor_id = fields.Many2one(comodel_name="hr.hospital.doctor")
    doctor_history_ids = fields.One2many(
        comodel_name="hr.hospital.doctor.history", inverse_name="patient_id"
    )
    visit_ids = fields.One2many(
        comodel_name="hr.hospital.visit", inverse_name="patient_id"
    )

    def action_view_patient_visits_history(self):
        self.ensure_one()
        return {
            "name": "Patient visits history",
            "type": "ir.actions.act_window",
            "res_model": "hr.hospital.visit",
            "view_mode": "list,form",
            "domain": [("patient_id", "=", self.id)],
        }

    def action_create_visit(self):
        self.ensure_one()
        return {
            "name": "New visit",
            "type": "ir.actions.act_window",
            "res_model": "hr.hospital.visit",
            "view_mode": "form",
            "target": "new",
            "context": {"default_patient_id": self.id},
        }
