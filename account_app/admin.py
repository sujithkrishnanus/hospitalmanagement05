from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(LoginTable)
admin.site.register(Specialization)
admin.site.register(DoctorRegistration)
admin.site.register(StaffRegistration)
admin.site.register(PatientRegistration)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Bill)
