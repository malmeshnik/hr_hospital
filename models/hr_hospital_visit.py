from odoo import models, fields


class HrHospitalVisit(models.Model):
    _name = "hr_hospital.visit"
    _description = "Visit"

    patient_id = fields.Many2one("hr_hospital.patient", string="Patient")
    doctor_id = fields.Many2one("hr_hospital.doctor", string="Doctor")
    desease_id = fields.Many2one("hr_hospital.desease", string="Desease")
    date = fields.Datetime(string="Visit Date", default=fields.Datetime.now)
