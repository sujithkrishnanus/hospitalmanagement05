from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from . models import *
from datetime import datetime
from django.utils import timezone
from decimal import Decimal
from .forms import *
import stripe

# Create your views here.

# ---------- For Home Page ----------

def home(request):
    return render(request, 'index.html')

# ---------- For registration, login, logout ----------

def patientRegistration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        gender = request.POST['gender']
        mobile_no = request.POST['mobile_no']
        address = request.POST['address']
        password = request.POST['password']
        password1 = request.POST['password1']

        if request.POST['password'] == request.POST['password1']:
            login_table, created = LoginTable.objects.get_or_create(user='patient', email=email,
                                                                    defaults={'password': password, 'password1': password1}
                                                                    )
            if created:
                patient = PatientRegistration(
                    type=login_table,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    mobile_no=mobile_no,
                    address=address
                )
                patient.save()

                messages.info(request, 'Registration success')
                return redirect('login')

            else:
                messages.info(request, 'Email already exists')
                return redirect('register')

        else:
            messages.info(request, 'Password not matching')
            return redirect('register')

    return render(request, 'patient_module/patient-reg.html')

def loginPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = LoginTable.objects.filter(email=email, password=password).first()

        if user is not None:
            request.session['email'] = email
            if user.user == 'patient':
                patient = PatientRegistration.objects.get(type=user)
                # request.session['email'] = email
                request.session['first_name'] = patient.first_name
                request.session['last_name'] = patient.last_name
                return redirect('patient_view')
            elif user.user == 'staff':
                staff = StaffRegistration.objects.get(type=user)
                # request.session['email'] = email
                request.session['first_name'] = staff.first_name
                request.session['last_name'] = staff.last_name
                return redirect('staff_view')
            elif user.user == 'doctor':
                doctor = DoctorRegistration.objects.get(type=user)
                request.session['first_name'] = doctor.first_name
                request.session['last_name'] = doctor.last_name
                return redirect('doctor_view')
        else:
            messages.error(request, 'invalid email or password')

    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    return redirect('/')

# ---------- For staff section ----------
def staffView(request):
    if 'email' in request.session:
        user = LoginTable.objects.get(email=request.session['email'])
        doctor_count = DoctorRegistration.objects.all().count
        specialization_count = Specialization.objects.all().count
        patient_count = PatientRegistration.objects.all().count
        reguser_count = LoginTable.objects.all().count
        staff = StaffRegistration.objects.get(type=user)
        first_name = staff.first_name
        last_name = staff.last_name
        context = {
            'doctor_count': doctor_count,
            'specialization_count': specialization_count,
            'patient_count': patient_count,
            'reguser_count': reguser_count,
            'user': user,
            'first_name': first_name,
            'last_name': last_name
        }
        return render(request,'admin/adminhome.html', context)
    else:
        # Handle the case where the email key is not set in the session
        return redirect('login')

            # ---------- (a) For specialization section ----------
def addSpecialization(request):
    user = LoginTable.objects.get(email=request.session['email'])
    if request.method == "POST":
        specializationname = request.POST.get('specializationname')
        specialization = Specialization(
            sname=specializationname,
        )
        specialization.save()
        messages.success(request, 'Specialization  Added Succeesfully!!!')
        return redirect("add_specilizations")
    return render(request, 'admin/specialization.html', {'user': user})

def viewSpecialization(request):
    specialization = Specialization.objects.all()
    user = LoginTable.objects.get(email=request.session['email'])
    context = {
        'specialization': specialization,
        'user': user
    }
    return render(request, 'admin/manage_specialization.html', context)

def updateSpecialization(request, id):
    specialization  = Specialization.objects.get(id=id)
    user = LoginTable.objects.get(email=request.session['email'])
    if request.method == 'POST':
        sname = request.POST.get('sname')
        specialization .sname = sname
        specialization .save()
        messages.success(request, "Your specialization detail has been updated successfully")
        return redirect('view_specilizations')
    return render(request, 'admin/update_specialization.html', {'specialization': specialization, 'user': user})

def deleteSpecialization(request, id):
    specialization = Specialization.objects.get(id=id)
    specialization.delete()
    messages.success(request, 'Record Delete Succeesfully!!!')

    return redirect('view_specilizations')

            # ---------- (b) For Doctor section ----------

def addDoctor(request):
    user = LoginTable.objects.get(email=request.session['email'])
    specialization = Specialization.objects.all()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        specialization_id = request.POST['specialization_id']
        mobile_no = request.POST['mobno']
        fee = request.POST['fees']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            try:
                specialization = Specialization.objects.get(id=specialization_id)
            except Specialization.DoesNotExist:
                messages.info(request, 'Invalid specialization')
                return redirect('register')

            login_table, created = LoginTable.objects.get_or_create(user='doctor', email=email)

            if created:
                login_table.password = password
                login_table.password1 = password1
                login_table.save()

            # Create DoctorRegistration object regardless of whether LoginTable object is created or not
            doctor, created = DoctorRegistration.objects.get_or_create(type=login_table,
                                                                      defaults={'first_name': first_name,
                                                                                'last_name': last_name,
                                                                                'specialization': specialization,
                                                                                'fee': fee,
                                                                                'mobile_no': mobile_no}
                                                                      )

            if created:
                messages.info(request, 'Registration success')
            else:
                messages.info(request, 'Doctor already exists')

            return redirect('doctorlist')

        else:
            messages.info(request, 'Password not matching')
            return redirect('register')

    return render(request, 'doc/docreg.html', {'specialization': specialization, 'user':user})

def viewDoctor(request):
    doctor = DoctorRegistration.objects.all()
    user = LoginTable.objects.get(email=request.session['email'])
    context = {
        'doctor': doctor,
        'user': user
    }
    return render(request, 'admin/doctor-list.html', context)

def updateDoctor(request, id):
    doctor = DoctorRegistration.objects.get(id=id)
    specialization = Specialization.objects.all()
    user = LoginTable.objects.get(email=request.session['email'])
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        specialization_id = request.POST.get('specialization_id')
        mobile_no = request.POST.get('mobile_no')
        fee = request.POST.get('fee')

        doctor.first_name = first_name
        doctor.last_name = last_name
        doctor.specialization_id = specialization_id
        doctor.fee = fee
        doctor.mobile_no = mobile_no

        doctor.save()
        messages.success(request, "Doctor detail has been updated successfully")
        return redirect('doctorlist')
    return render(request, 'admin/doctor_update.html', {'doctor': doctor, 'user': user, 'specialization': specialization})

def deleteDoctor(request, id):
    doctor = DoctorRegistration.objects.get(id=id)
    doctor.delete()
    messages.success(request, 'Record Delete Succeesfully!!!')

    return redirect('doctorlist')


                # ---------- (c) For Patient section ----------

def allPatientDisplay(request):
    user = LoginTable.objects.get(email=request.session['email'])
    patients = PatientRegistration.objects.all()
    context = {
        'patients': patients,
        'user': user
    }
    return render(request, 'admin/reg-users.html', context)

def specificPatientAppointment(request, id):
    patient = PatientRegistration.objects.get(id=id)
    user = LoginTable.objects.get(email=request.session['email'])
    appointments = Appointment.objects.filter(pat_id=patient)
    context = {
        'patient': patient,
        'appointments': appointments,
        'user': user
    }
    return render(request, 'admin/reg_users_appointment.html', context)

def patient_appointment_details(request, id, appointment_id):
    patient = PatientRegistration.objects.get(id=id)
    appointment = Appointment.objects.get(pat_id=patient, id=appointment_id)
    user = LoginTable.objects.get(email=request.session['email'])
    bills = Bill.objects.filter(patient=patient, appointment=appointment)
    all_bills_paid = all(bill.payment_status == 'Paid' for bill in bills) if bills.exists() else False


    context = {
        'appointment': appointment,
        'user': user,
        'all_bills_paid': all_bills_paid
    }
    return render(request, 'doc/patient_appointment_details.html', context)

def update_appointment_status(request, patient_id, appointment_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = status
            appointment.save()
            messages.success(request, "Appointment status updated successfully")
            return redirect('specific_patient', id=patient_id)
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found")
            return redirect('specific_patient', id=patient_id)
    else:
        return HttpResponseNotAllowed(['POST'])

                # ---------- (c) For Payment section ----------


def createBill(request, patient_id, appointment_id):
    user = LoginTable.objects.get(email=request.session['email'])
    patient = PatientRegistration.objects.get(id=patient_id)
    appointment = Appointment.objects.get(id=appointment_id)
    doctor = appointment.doctor_id

    bills = Bill.objects.filter(patient=patient, appointment=appointment)

    total_amount = sum(b.total_price for b in bills)

    doctor_fee = doctor.fee

    # Check if there are any bills and get the payment status of the first bill
    all_bills_paid = bills.exists() and all(bill.payment_status == 'Paid' for bill in bills)

    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.patient = patient
            bill.doctor = doctor
            bill.appointment = appointment

            # Calculate the new total price for this bill
            bill.total_price = form.cleaned_data['total_price']
            bill.save()

            # Recalculate the total amount including the new bill
            total_amount += bill.total_price

            messages.success(request, 'Bill added successfully')
            return redirect('view_bills', patient_id=patient_id, appointment_id=appointment_id)
    else:
        form = BillForm()

    # Add the doctor's fee to the total amount only once
    total_amount += doctor_fee

    context = {
        'form': form,
        'patient': patient,
        'appointment': appointment,
        'doctor': doctor,
        'user': user,
        'bills': bills,
        'total_amount': total_amount,
        'doctor_fee': doctor_fee,
        'all_bills_paid': all_bills_paid,
    }
    return render(request, 'admin/bill.html', context)


# ---------- For doctor section ----------
def doctorView(request):
    user = LoginTable.objects.get(email=request.session['email'])
    doctor = DoctorRegistration.objects.get(type=user)
    allaptcount = Appointment.objects.filter(doctor_id=doctor).count()
    approptcount = Appointment.objects.filter(status='Approved', doctor_id=doctor).count()
    first_name = doctor.first_name
    last_name = doctor.last_name
    context = {
        'allaptcount': allaptcount,
        'first_name': first_name,
        'last_name': last_name,
        'user': user,
        'approptcount': approptcount,
    }
    return render(request, 'doc/dochome.html', context)

def allPatientViewDoctor(request):
    user = LoginTable.objects.get(email=request.session['email'])
    doctor = DoctorRegistration.objects.get(type=user)
    appropatient = Appointment.objects.filter(status='Approved', doctor_id=doctor)
    context = {'user': user,
               'appropatient': appropatient
    }
    return render(request, 'doc/view_appointment.html', context)

def singlePatientViewDoctor(request, id, appointment_id):
    patient = PatientRegistration.objects.get(id=id)
    appointment = Appointment.objects.get(pat_id=patient, id=appointment_id)
    user = LoginTable.objects.get(email=request.session['email'])
    context = {
        'appointment': appointment,
        'user': user,
    }
    return render(request, 'doc/single_patient_view.html', context)

def prescription(request, patient_id, appointment_id):
    patient = PatientRegistration.objects.get(id=patient_id)
    appointment = Appointment.objects.get(id=appointment_id)
    prescr = Prescription.objects.filter(patient=patient, appointment=appointment)
    user = LoginTable.objects.get(email=request.session['email'])
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient
            prescription.appointment = appointment
            prescription.save()
            messages.success(request, 'Prescription added successfully')
            return redirect('prescription', patient_id=patient_id, appointment_id=appointment_id)
    else:
        form = PrescriptionForm()

    context = {'form': form,
               'patient': patient,
               'appointment': appointment,
               'prescr': prescr,
               'user': user
    }
    return render(request, 'doctor_module/e_prescribing.html', context)

# ---------- For patient section ----------
def patientView(request):
    first_name = request.session['first_name']
    last_name = request.session['last_name']
    user = LoginTable.objects.get(email=request.session['email'])
    patient = PatientRegistration.objects.get(type=user)
    request.session['patient_id'] = patient.id
    context = {'first_name': first_name,
               'last_name': last_name,
               'user': user,
               'patient': patient
    }
    return render(request, 'user/userhome.html', context)

            # ---------- (a) For create appointment ----------

def createAppointment(request):
    specialization = Specialization.objects.all()
    doctor_name = DoctorRegistration.objects.all()
    user = LoginTable.objects.get(email=request.session['email'])

    if request.method == "POST":
        try:
            spec_id = request.POST.get('spec_id')
            doctor_id = request.POST.get('doctor_id')
            date_of_appointment = request.POST.get('date_of_appointment')
            time_of_appointment = request.POST.get('time_of_appointment')
            additional_msg = request.POST.get('additional_msg')

            # Retrieve the DoctorReg and Specialization instances
            doc_instance = DoctorRegistration.objects.get(id=doctor_id)
            spec_instance = Specialization.objects.get(id=spec_id)

            # Accessing the PatientReg instance associated with the logged-in user
            patient_instance = PatientRegistration.objects.get(type=user)

            # Validate that date_of_appointment is greater than today's date
            try:
                appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
                today_date = timezone.now().date()

                if appointment_date <= today_date:
                    # If the appointment date is not in the future, display an error message
                    messages.error(request, "Please select a date in the future for your appointment")
                    return redirect('patientappointment')  # Redirect back to the appointment page
            except ValueError:
                # Handle invalid date format error
                messages.error(request, "Invalid date format")
                return redirect('patientappointment')  # Redirect back to the appointment page

            # Create a new Appointment instance with the provided data
            Appointment.objects.create(
                pat_id=patient_instance,
                spec_id=spec_instance,
                doctor_id=doc_instance,
                date_of_appointment=date_of_appointment,
                time_of_appointment=time_of_appointment,
                additional_msg=additional_msg
            )

            # Display a success message
            messages.success(request, "Your Appointment Request Has Been Sent. We Will Contact You Soon")
            return redirect('patientappointment')

        except DoctorRegistration.DoesNotExist:
            messages.error(request, "Selected doctor does not exist.")
        except Specialization.DoesNotExist:
            messages.error(request, "Selected specialization does not exist.")
        except PatientRegistration.DoesNotExist:
            messages.error(request, "Patient information could not be retrieved.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('patientappointment')  # Redirect back to the appointment page in case of an error

    context = {
        'specialization': specialization,
        'user': user,
        'doctor_name': doctor_name
    }
    return render(request, 'user/appointment.html', context)


def get_doctor(request):
    if request.method == 'GET':
        s_id = request.GET.get('s_id')
        doctors = DoctorRegistration.objects.filter(specialization_id=s_id)

        doctor_options = ''
        for doc in doctors:
            doctor_options += f'<option value="{doc.id}">{doc.first_name} {doc.last_name}</option>'

        return JsonResponse({'doctor_options': doctor_options})

def appointmentView(request, patient_id):
    patient = PatientRegistration.objects.get(id=patient_id)
    appointments = Appointment.objects.filter(pat_id=patient)
    user = LoginTable.objects.get(email=request.session['email'])
    context = {
        'appointments': appointments,
        'user':user,
        'patient': patient
    }
    return render(request, 'user/appointment-history.html', context)

def cancelAppointment(request, id):
    appointment = Appointment.objects.get(id=id)
    patient_id = appointment.pat_id.id
    appointment.status = 'Canceled'
    appointment.delete()
    messages.success(request, 'Appointment Deleted Successfully!!!')
    return redirect('appointment_history', patient_id=patient_id)

def paymentBill(request, patient_id, appointment_id):
    patient = PatientRegistration.objects.get(id=patient_id)
    appointment = Appointment.objects.get(id=appointment_id)
    bills = Bill.objects.filter(patient=patient, appointment=appointment)
    doctor = appointment.doctor_id
    total_amount = sum(b.total_price for b in bills)
    doctor_fee = doctor.fee
    total_amount += doctor_fee
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if bills.exists():
        line_items = []
        line_item = {
            'price_data': {
                'currency': 'INR',
                'unit_amount': int(total_amount * 100),
                'product_data': {
                    'name': 'Payment Your Bill '
                }
            },
            'quantity': 1
        }
        line_items.append(line_item)


        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('cancel'))
        )
        request.session['appointment_id'] = appointment_id
        request.session['patient_id'] = patient_id
        return redirect(checkout_session.url, code=303)

    return HttpResponse('Error: Bill not generated by staff')


def success(request):
    appointment_id = request.session.get('appointment_id')
    patient_id = request.session.get('patient_id')

    bills = Bill.objects.filter(patient_id=patient_id, appointment_id=appointment_id)
    for bill in bills:
        bill.payment_status = 'Paid'
        bill.save()
    return render(request, 'admin/success.html')

def cancel(request):
    return render(request, 'admin/cancel.html')