from odoo import models, fields


class HrHospitalDoctor(models.Model):
    _name = "hr_hospital.doctor"
    _description = "Doctor"

    name = fields.Char()
    specialization = fields.Char()
    patient_ids = fields.Many2many("hr_hospital.patient", string="patients")
