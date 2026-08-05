from odoo import models, fields, api


class HrHospitalDoctorhistory(models.Model):
    _name = "hr.hospital.doctor.history"
    _description = "Doctor History"

    patient_id = fields.Many2one("hr.hospital.patient", required=True)
    doctor_id = fields.Many2one("hr.hospital.doctor", required=True)
    assign_date = fields.Date(required=True, default=fields.Date.today())
    end_date = fields.Date()
    active = fields.Boolean(default=True)

    @api.onchange("assign_date", "end_date")
    def _onchange_dates_check(self):
        for record in self:
            if record.assign_date and record.end_date:
                if record.assign_date > record.end_date:
                    return {
                        "warning": {
                            "title": "Помилка дат",
                            "message": "Дата призначення не може бути пізніше дати закінчення.",
                        }
                    }

    def _compute_display_name(self):
        for record in self:
            category = record.doctor_id.category_id.name or ""
            date_str = (
                record.assign_date.strftime("%d.%m.%Y") if record.assign_date else ""
            )

            record.display_name = f"{record.patient_id.name} - {record.doctor_id.name}({category}) - {date_str}"
