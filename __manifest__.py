{
    "name": "Hr Hospital",
    "version": "19.0.1.0.0",
    "depends": ["base"],
    "author": "Malme",
    "data": [
        "security/ir.model.access.csv",
        #
        "wizard/hr_hospital_mass_reassign_doctor_wizard_view.xml",
        "wizard/hr_hospital_visit_report_wizard_view.xml",
        #
        "views/hr_hospital_doctor_category_views.xml",
        "views/hr_hospital_doctor_history_views.xml",
        "views/hr_hospital_menu.xml",
        "views/hr_hospital_doctor_views.xml",
        "views/hr_hospital_patient_views.xml",
        "views/hr_hospital_desease_views.xml",
        "views/hr_hospital_visit_views.xml",
        #
        "demo/hr_hospital_desease_data.xml",
        "demo/hr_hostpital_doctor_category_data.xml",
    ],
    "demo": [
        "demo/hr_hospital_doctor_demo.xml",
        "demo/hr_hospital_patient_demo.xml",
        "demo/hr_hospital_doctor_history_demo.xml",
        "demo/hr_hospital_visit_demo.xml",
    ],
}
