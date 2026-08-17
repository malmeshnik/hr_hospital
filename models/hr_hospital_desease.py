from odoo import models, fields, api


class HrHospitalDesease(models.Model):
    """Model representing a disease classifier with a hierarchical structure.

    Supports parent-child classification utilizing parent_store for efficient
    retrieval of tree-structured data.
    """

    _name = "hr.hospital.desease"
    _description = "Desease"
    _parent_store = True
    _parent_name = "parent_id"

    name = fields.Char()
    description = fields.Text()

    parent_id = fields.Many2one(
        comodel_name="hr.hospital.desease", index=True, ondelete="restrict"
    )
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many(
        comodel_name="hr.hospital.desease",
        inverse_name="parent_id",
    )

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        """Verify that the disease hierarchy does not contain cyclic dependencies.

        Raises:
            ValidationError: If a disease record references itself or creates
                a recursive cycle among its ancestor records.
        """
        if self._has_cycle():
            raise Exception(
                "Cannot save: a desease record cannot be its own ancestor (recursive hierarchy detected)."
            )

    def _compute_display_name(self):
        """Compute the display name for disease records including their full hierarchy path."""
        for desease in self:
            desease.display_name = desease._get_hierarchy_display_name()

    def _get_hierarchy_display_name(self):
        """Recursively build the hierarchical display name path for the record.

        Returns:
            str: The formatted hierarchy path string separated by slashes (e.g., "Category / Disease").
        """
        self.ensure_one()
        if self.parent_id:
            return f"{self.parent_id._get_hierarchy_display_name()} / {self.name}"
        return self.name
