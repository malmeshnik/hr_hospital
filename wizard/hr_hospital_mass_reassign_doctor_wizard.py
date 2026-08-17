from odoo import models, fields


class HrHospitalMassReassignDoctorWizard(models.TransientModel):
    """Wizard model for mass reassigning a primary personal doctor to selected patients.

    Designed to be called from the Patient list view with active context records.
    """

    _name = "hr.hospital.mass.reassign.doctor.wizard"
    _description = "Mass Reassign Personal Doctor for Patients"

    new_doctor_id = fields.Many2one(comodel_name="hr.hospital.doctor", required=True)
    change_date = fields.Date(default=fields.Date.today())

    def action_reassign_doctor(self):
        """Mass update the assigned personal doctor for all selected patient records.

        Retrieves selected active IDs from context, validates the source model,
        and updates the doctor_id field for each patient.

        Returns:
            dict: An ir.actions.act_window_close action dictionary to close the wizard dialog.

        Raises:
            Exception: If launched outside the hr.hospital.patient model or with no active records selected.
        """
        
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
