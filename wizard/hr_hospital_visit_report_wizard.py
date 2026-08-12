from datetime import datetime, time
from odoo import api, fields, models


class HrHospitalVisitReportWizard(models.TransientModel):
    _name = "hr.hospital.visit.report.wizard"
    _description = "Patient Visits Report Wizard"

    doctor_ids = fields.Many2many(comodel_name="hr.hospital.doctor")
    patient_ids = fields.Many2many(comodel_name="hr.hospital.patient")
    start_date = fields.Date()
    end_date = fields.Date()
    is_completed_visits = fields.Boolean()
    desease_id = fields.Many2one(comodel_name="hr.hospital.desease")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        active_model = self.env.context.get("active_model")
        active_ids = self.env.context.get("active_ids")

        if active_model == "hr.hospital.doctor" and "doctor_ids" in fields_list:
            res["doctor_ids"] = [(6, 0, active_ids)]

            doctors = self.env["hr.hospital.doctor"].browse(active_ids)
            patient_ids = doctors.mapped("patient_ids").ids

            res["patient_ids"] = [(6, 0, patient_ids)]
        elif active_model == "hr.hospital.patient" and "patient_ids" in fields_list:
            res["patient_ids"] = [(6, 0, active_ids)]

            patients = self.env["hr.hospital.patient"].browse(active_ids)
            doctor_ids = patients.mapped("doctor_id").ids

            res["doctor_ids"] = [(6, 0, doctor_ids)]

        return res

    def action_generate_report(self):
        self.ensure_one()

        domain = []

        if self.doctor_ids:
            domain.append(("doctor_id", "in", self.doctor_ids.ids))
        if self.patient_ids:
            domain.append(("patient_id", "in", self.patient_ids.ids))
        if self.start_date:
            start_datetime = datetime.combine(self.start_date, time.min)
            domain.append(("visit_datetime", ">=", start_datetime))
        if self.end_date:
            end_datetime = datetime.combine(self.end_date, time.max)
            domain.append(("visit_datetime", "<=", end_datetime))
        if self.is_completed_visits:
            domain.append(("status", "=", "done"))
        if self.desease_id:
            domain.append(("deaseas_id", "=", self.desease_id.id))

        return {
            "type": "ir.actions.act_window",
            "name": "Patient visits report",
            "res_model": "hr.hospital.visit",
            "view_mode": "list",
            "domain": domain,
            "target": "current",
        }
