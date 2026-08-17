from odoo import models, fields, api


class HrHospitalDoctor(models.Model):
    """Model representing a medical doctor in the hospital.

    Inherits medical background info from hr.hospital.medic.info and manages
    doctor-patient links, specialty categories, and mentor-intern relationships.
    """

    _name = "hr.hospital.doctor"
    _description = "Doctor"
    _inherit = "hr.hospital.medic.info"

    name = fields.Char()
    specialization = fields.Char()
    active = fields.Boolean(default=True)
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
        """Compute whether the doctor is an intern based on their assigned category."""
        for doctor in self:
            doctor.is_intern = doctor.category_id.id == 1

    @api.constrains("mentor_id")
    def _check_mentor_not_intern(self):
        """Verify that an assigned mentor is not an intern.

        Raises:
            Exception: If the selected mentor doctor is flagged as an intern.
        """
        
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise Exception("The doctor can't be mentor, because his intern")
