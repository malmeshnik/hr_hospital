from datetime import date
from odoo import fields
from odoo.tests.common import TransactionCase


class TestHospitalMethods(TransactionCase):

    def setUp(self):
        super().setUp()

        self.category_intern = self.env['hr.hospital.doctor.category'].create({
            'name': 'Інтерн',
        })
        self.category_spec = self.env['hr.hospital.doctor.category'].create({
            'name': 'Спеціаліст',
        })

        self.doctor_intern = self.env['hr.hospital.doctor'].create({
            'name': 'Д-р Інтернов',
            'category_id': self.category_intern.id,
        })
        self.doctor_senior = self.env['hr.hospital.doctor'].create({
            'name': 'Д-р Старший',
            'category_id': self.category_spec.id,
        })

        self.patient = self.env['hr.hospital.patient'].create({
            'name': 'Іван Іванов',
            'birth_date': date(2000, 1, 1),
        })

    def test_01_compute_age(self):
        today = fields.Date.context_today(self.patient)
        expected_age = today.year - 2000 - ((today.month, today.day) < (1, 1))
        self.assertEqual(self.patient.age, expected_age)

    def test_02_mentor_intern_constraint(self):
        self.doctor_intern.category_id = 1
        self.doctor_intern._compute_is_intern()

        with self.assertRaises(Exception):
            self.doctor_senior.write({
                'mentor_id': self.doctor_intern.id
            })

    def test_03_visit_write_and_unlink_protection(self):
        visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor_senior.id,
            'visit_datetime': fields.Datetime.now(),
        })

        with self.assertRaises(Exception):
            visit.write({'doctor_id': self.doctor_intern.id})

        with self.assertRaises(Exception):
            visit.unlink()