from odoo import models, fields, api


class HrHospitalDesease(models.Model):
    _name = "hr.hospital.desease"
    _description = "Desease"
    _parent_store = True
    _parent_name = "parent_id"

    name = fields.Char()
    description = fields.Text()

    parent_id = fields.Many2one(
        comodel_name="hr.hospital.desease", index=True, ondelete="restrict"
    )
    parent_path = fields.Char(index=True, unaccent=False)
    child_ids = fields.One2many(
        comodel_name="hr.hospital.desease",
        inverse_name="parent_id",
    )

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        if self._has_cycle():
            raise Exception(
                "Cannot save: a desease record cannot be its own ancestor (recursive hierarchy detected)."
            )

    def _compute_display_name(self):
        for desease in self:
            desease.display_name = desease._get_hierarchy_display_name()

    def _get_hierarchy_display_name(self):
        self.ensure_one()
        if self.parent_id:
            return f"{self.parent_id._get_hierarchy_display_name()} / {self.name}"
        return self.name
