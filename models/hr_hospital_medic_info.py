from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class HrHospitalMedicInfo(models.AbstractModel):
    _name = "hr.hospital.medic.info"
    _description = "Medic Info"

    blood_type = fields.Selection(
        selection=[
            ("o_plus", "O(I) Rh+"),
            ("o_minus", "O(I) Rh-"),
            ("a_plus", "A(II) Rh+"),
            ("a_minus", "A(II) Rh-"),
            ("b_plus", "B(III) Rh+"),
            ("b_minus", "B(III) Rh-"),
            ("ab_plus", "AB(IV) Rh+"),
            ("ab_minus", "AB(IV) Rh-"),
        ]
    )
    gender = fields.Selection(selection=[("male", "Male"), ("female", "Female")])
    birth_date = fields.Date()
    age = fields.Integer(compute="_compute_age")

    @api.depends("birth_date")
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.birth_date:
                record.age = relativedelta(today, record.birth_date).years
            else:
                record.age = 0
