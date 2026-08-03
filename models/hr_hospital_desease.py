from odoo import models, fields


class HrHospitalDesease(models.Model):
    _name = "hr_hospital.desease"
    _description = "Desease"

    name = fields.Char()
    description = fields.Text()
