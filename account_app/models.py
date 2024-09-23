from django.db import models

# Create your models here.
class LoginTable(models.Model):
    USER = {
        ('staff', 'staff'),
        ('doctor', 'doctor'),
        ('patient', 'patient'),
    }

    user = models.CharField(choices=USER, max_length=200, default='patient')
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    password1 = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.email)

class Specialization(models.Model):
    sname = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.sname)

class DoctorRegistration(models.Model):
    type = models.OneToOneField(LoginTable, on_delete=models.CASCADE, limit_choices_to={'user': 'doctor'})
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mobile_no = models.IntegerField(unique=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class StaffRegistration(models.Model):
    type = models.OneToOneField(LoginTable, on_delete=models.CASCADE, limit_choices_to={'user': 'staff'})
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    staff_id = models.IntegerField(unique=True)
    mobile_no = models.IntegerField(unique=True)

    def __str__(self):
        return '{}'.format(self.first_name)

class PatientRegistration(models.Model):
    type = models.OneToOneField(LoginTable, on_delete=models.CASCADE, limit_choices_to={'user': 'patient'})
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=100)
    mobile_no = models.IntegerField(unique=True)
    address = models.TextField()

    def __str__(self):
        return '{}'.format(self.first_name)


class Appointment(models.Model):
    STATUS_CHOICES = [
        (0, 0),
        ('Approved', 'Approved'),
        ('Canceled', 'Canceled'),
    ]
    spec_id = models.ForeignKey(Specialization, on_delete=models.CASCADE, default=0)
    pat_id = models.ForeignKey(PatientRegistration, on_delete=models.CASCADE, default=0)
    date_of_appointment = models.CharField(max_length=250)
    time_of_appointment = models.CharField(max_length=250)
    doctor_id = models.ForeignKey(DoctorRegistration, on_delete=models.CASCADE)
    additional_msg = models.TextField(blank=True)
    remark = models.CharField(max_length=250, default=0)
    status = models.CharField(default=0, max_length=200, choices=STATUS_CHOICES)

    def __str__(self):
        return '{}'.format(self.doctor_id)

class Prescription(models.Model):
    patient = models.ForeignKey(PatientRegistration, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    instructions = models.TextField()
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.patient, self.medicine)

class Bill(models.Model):
    patient = models.ForeignKey(PatientRegistration, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorRegistration, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=200, choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ], default='Pending')

    def __str__(self):
        return f'Bill for {self.patient.first_name}  {self.patient.last_name}'

