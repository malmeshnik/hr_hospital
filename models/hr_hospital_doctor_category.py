from odoo import models, fields, api


class HrHospitalDoctorCategory(models.Model):
    _name = "hr.hospital.doctor.category"
    _description = "Doctor Category"

    name = fields.Char()
    sequence = fields.Integer()
    doctor_ids = fields.One2many(
        comodel_name="hr.hospital.doctor",
        inverse_name="category_id",
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "The name of the doctor category must be unique.",
        )
    ]
