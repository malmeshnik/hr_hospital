from odoo import models, fields, api


class HrHospitalDoctor(models.Model):
    _name = "hr.hospital.doctor"
    _description = "Doctor"
    _inherit = "hr.hospital.medic.info"

    name = fields.Char()
    specialization = fields.Char()
    is_intern = fields.Boolean(store=True, compute="_compute_is_intern")

    patient_ids = fields.Many2many(comodel_name="hr.hospital.patient")

    category_id = fields.Many2one(comodel_name="hr.hospital.doctor.category")
    system_user = fields.Many2one(comodel_name="res.users")
    mentor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor", domain="[('is_intern', '=', False)]"
    )
    intern_ids = fields.One2many(
        comodel_name="hr.hospital.doctor",
        inverse_name="mentor_id",
    )

    @api.depends("category_id")
    def _compute_is_intern(self):
        for doctor in self:
            doctor.is_intern = doctor.category_id.id == 1

    @api.constrains("mentor_id")
    def _check_mentor_not_intern(self):
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise Exception("The doctor can't be mentor, because his intern")
