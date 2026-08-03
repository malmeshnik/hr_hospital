from odoo import models, fields


class HrHospitalPatient(models.Model):
    _name = "hr_hospital.patient"
    _description = "Patient"

    name = fields.Char()

    doctor_id = fields.Many2one("hr_hospital.doctor", string="Doctor")
    visit_ids = fields.One2many("hr_hospital.visit", "patient_id", string="Visits")
