from odoo import models, fields


class HrHospitalMassReassignDoctorWizard(models.TransientModel):
    _name = "hr.hospital.mass.reassign.doctor.wizard"
    _description = "Mass Reassign Personal Doctor for Patients"

    new_doctor_id = fields.Many2one(comodel_name="hr.hospital.doctor", required=True)
    change_date = fields.Date(default=fields.Date.today())

    def action_reassign_doctor(self):
        self.ensure_one()

        active_model = self.env.context.get("active_model")
        active_ids = self.env.context.get("active_ids")

        if active_model != "hr.hospital.patient" or not active_ids:
            raise Exception(
                "This wizard must be launched from the Patient list view "
                "with at least one patient selected."
            )

        patients = self.env["hr.hospital.patient"].browse(active_ids)
        patients.write({"doctor_id": self.new_doctor_id.id})

        return {"type": "ir.actions.act_window_close"}
