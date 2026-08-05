from odoo import models, fields


class HrHospitalPatient(models.Model):
    _name = "hr.hospital.patient"
    _description = "Patient"
    _inherit = "hr.hospital.medic.info"

    name = fields.Char()
    insurance_number = fields.Char(size=20)

    doctor_id = fields.Many2one(comodel_name="hr.hospital.doctor")
    doctor_history_ids = fields.One2many(
        comodel_name="hr.hospital.doctor.history", inverse_name="patient_id"
    )
    visit_ids = fields.One2many(
        comodel_name="hr.hospital.visit", inverse_name="patient_id"
    )
