from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.patientRegistration, name='register'),
    path('logout/', views.logoutPage, name='logout'),

    path('patient_view/', views.patientView, name='patient_view'),
    path('staff_view/', views.staffView, name='staff_view'),
    path('doctor_view/', views.doctorView, name='doctor_view'),
    path('patientappointment', views.createAppointment, name='patientappointment'),
    path('get_doctor/', views.get_doctor, name='get_doctor'),
    path('appointment_history/<int:patient_id>/', views.appointmentView, name='appointment_history'),

    # Specialization

    path('add_specilizations', views.addSpecialization, name='add_specilizations'),
    path('view_specilizations', views.viewSpecialization, name='view_specilizations'),
    path('updateSpecialization/<int:id>/', views.updateSpecialization, name='updateSpecialization'),
    path('deleteSpecialization/<int:id>/', views.deleteSpecialization, name='deleteSpecialization'),

    path('docregister', views.addDoctor, name='docregister'),
    path('doctorlist', views.viewDoctor, name='doctorlist'),
    path('updatedoctor/<int:id>/', views.updateDoctor, name='updatedoctor'),
    path('doctordelete/<int:id>/', views.deleteDoctor, name='doctordelete'),

    path('all_patient', views.allPatientDisplay, name='all_patient'),
    path('specific_patient/<int:id>/', views.specificPatientAppointment, name='specific_patient'),
    path('statusupdate/<int:id>/<int:appointment_id>/', views.patient_appointment_details, name='statusupdate'),
    path('update_appointment_status/<int:patient_id>/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    path('delete_appointment/<int:id>/', views.cancelAppointment, name='delete_appointment'),
    path('patientviewdoctor', views.allPatientViewDoctor, name='patientviewdoctor'),
    path('singlepatient/<int:id>/<int:appointment_id>/', views.singlePatientViewDoctor, name='singlepatient'),
    path('prescription/<int:patient_id>/<int:appointment_id>/', views.prescription, name='prescription'),
    path('view_bills/<int:patient_id>/<int:appointment_id>/', views.createBill, name='view_bills'),
    path('payment_bill/<int:patient_id>/<int:appointment_id>/', views.paymentBill, name='payment_bill'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
]