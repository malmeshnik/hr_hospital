from odoo import models, fields


class HrHospitalDoctorCategory(models.Model):
    """Model representing doctor qualification categories.

    Defines category levels (e.g., Intern, Specialist) with ordering options
    and manages links to associated doctor records.
    """
    _name = "hr.hospital.doctor.category"
    _description = "Doctor Category"

    name = fields.Char()
    sequence = fields.Integer()
    doctor_ids = fields.One2many(
        comodel_name="hr.hospital.doctor",
        inverse_name="category_id",
    )

    _name_uniq = models.Constraint(
        "unique(name)",
        "This name already exists!",
    )
