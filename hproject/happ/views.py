from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import AdminSigupForm, PatientForm, DoctorForm, StaffForm, DepartmentForm,AppointmentForm,StaffAppointmentForm,PrescriptionForm,MedicineForm,BillingForm
from .models import Feedback, Patient,Doctor,Staff,Department,Appointment,Prescription,Medicine,Billing
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




# ================= PATIENT SIGNUP =================



def home(request):
    return render(request, 'index.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        message = request.POST.get('message')
        rating = request.POST.get('rating')

        Feedback.objects.create(
            name=name,
            message=message,
            rating=rating
        )

        return redirect('feedback_list')

    return render(request, "contactus.html")


def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-id')
    return render(request, "feedback_list.html", {
        "feedbacks": feedbacks
    })



#for showing signup/login button for doctor
def adminclick_view(request):
    return render(request,'adminclick.html')

def doctorclick_view(request):
    return render(request,'doctorclick.html')

def patientclick_view(request):
    return render(request,'patientclick.html')

def staffclick_view(request):
    return render(request, 'staffclick.html')


def admin_signup(request):

    form = AdminSigupForm()

    if request.method == 'POST':

        form = AdminSigupForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']

            # Username already exists check
            if User.objects.filter(username=username).exists():

                messages.error(
                    request,
                    "Admin already registered with this username"
                )

                return render(
                    request,
                    'adminsignup.html',
                    {'form': form}
                )

            # Save admin user
            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            # Create admin group
            my_admin_group, created = Group.objects.get_or_create(
                name='admin'
            )

            my_admin_group.user_set.add(user)

            messages.success(
                request,
                "Admin Registered Successfully"
            )

            return redirect('admin_login')

    return render(
        request,
        'adminsignup.html',
        {'form': form}
    )



def patient_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('patient_dashboard')   # 👈 MUST
        else:
            return render(request, 'patient_login.html', {'error': 'Invalid credentials'})

    return render(request, 'patient_login.html')

# DOCTOR LOGIN
def doctor_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # check Doctor group
            if user.groups.filter(name='Doctor').exists():
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                return render(request, 'doctor_login.html',
                              {'error': 'You are not registered as Doctor'})
        else:
            return render(request, 'doctor_login.html',
                          {'error': 'Invalid username or password'})

    return render(request, 'doctor_login.html')


def staff_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # check Staff group
            if user.groups.filter(name='Staff').exists():
                login(request, user)
                return redirect('staff_dashboard')
            else:
                return render(request, 'staff_login.html',
                              {'error': 'You are not registered as Staff'})
        else:
            return render(request, 'staff_login.html',
                          {'error': 'Invalid username or password'})

    return render(request, 'staff_login.html')



# ADMIN LOGIN

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # check Admin group
            if user.groups.filter(name='ADMIN').exists():
                login(request, user)
                return redirect('admin_dashboard')

            else:
                return render(
                    request,
                    'admin_login.html',
                    {
                        'error': 'You are not registered as Admin'
                    }
                )

        else:
            return render(
                request,
                'admin_login.html',
                {
                    'error': 'Invalid username or password'
                }
            )

    return render(request, 'admin_login.html')
# ================= PATIENT SIGNUP =================

def patient_signup(request):
    form = PatientForm()

    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already registered")
                return render(request, "patient_signup.html", {"form": form})

            # Email already exists
            if Patient.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return render(request, "patient_signup.html", {"form": form})

            # Create Django User
            user = User.objects.create_user(
                username=username,
                password=password
            )

            # Add group
            group, created = Group.objects.get_or_create(name='Patient')
            user.groups.add(group)

            # Save patient
            obj = form.save(commit=False)
            obj.username = username
            obj.password = make_password(password)
            obj.save()

            messages.success(request, "Patient Registered Successfully")
            return redirect('patient_login')

    return render(request, "patient_signup.html", {"form": form})


# ================= DOCTOR SIGNUP =================

def doctor_signup(request):
    form = DoctorForm()

    if request.method == "POST":
        form = DoctorForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already registered")
                return render(request, "doctor_signup.html", {"form": form})

            # Email exists
            if Doctor.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return render(request, "doctor_signup.html", {"form": form })

            # Create User
            user = User.objects.create_user(
                username=username,
                password=password
            )

            # Add group
            group, created = Group.objects.get_or_create(name='Doctor')
            user.groups.add(group)

            # Save doctor
            obj = form.save(commit=False)
            obj.username = username
            obj.password = make_password(password)
            obj.save()

            messages.success(request, "Doctor Registered Successfully")
            return redirect("doctor_login")

    return render(request, "doctor_signup.html", {"form": form})


# ================= STAFF SIGNUP =================

def staff_signup(request):
    form = StaffForm()

    if request.method == "POST":
        form = StaffForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already registered")
                return render(request, "staff_signup.html", {"form": form})

            # Email exists
            if Staff.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return render(request, "staff_signup.html", {"form": form})

            # Create User
            user = User.objects.create_user(
                username=username,
                password=password
            )

            # Add group
            group, created = Group.objects.get_or_create(name='Staff')
            user.groups.add(group)

            # Save staff
            obj = form.save(commit=False)
            obj.username = username
            obj.password = make_password(password)
            obj.save()

            messages.success(request, "Staff Registered Successfully")
            return redirect("staff_login")

    return render(request, "staff_signup.html", {"form": form})


# ================= ADD DEPARTMENT =================
def add_department(request):
    form = DepartmentForm()

    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department Added Successfully")
            return redirect('department_list')

    return render(request, "add_department.html", {"form": form})


# ================= VIEW DEPARTMENT =================
def view_department(request):
    departments = Department.objects.all()
    return render(request, "view_department.html", {"departments": departments})



def login_view(request):

    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        role=request.POST.get("role")   # dropdown role

        user=authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # role validation
            if role=="patient" and not user.groups.filter(name='Patient').exists():
                messages.error(request,"Invalid Patient Login")
                return redirect('login')

            elif role=="doctor" and not user.groups.filter(name='Doctor').exists():
                messages.error(request,"Invalid Doctor Login")
                return redirect('login')

            elif role=="staff" and not user.groups.filter(name='Staff').exists():
                messages.error(request,"Invalid Staff Login")
                return redirect('login')

            login(request,user)

            # correct redirect
            if user.groups.filter(name='Patient').exists():
                return redirect('patient_dashboard')

            elif user.groups.filter(name='Doctor').exists():
                return redirect('doctor_dashboard')

            elif user.groups.filter(name='Staff').exists():
                return redirect('staff_dashboard')

        else:
            messages.error(
                request,
                "Invalid username or password"
            )

    return render(request,"login.html")



def logout_view(request):
    logout(request)
    return redirect('login')


def patient_dashboard(request):
    patient = Patient.objects.get(username=request.user.username)

    appointments = Appointment.objects.filter(patient=patient)

    total_appointments = appointments.count()
    pending_count = appointments.filter(status="Pending").count()
    completed_count = appointments.filter(status="Completed").count()

    return render(request, 'patient_dashboard.html', {
        'appointments': appointments,
        'total_appointments': total_appointments,
        'pending_count': pending_count,
        'completed_count': completed_count,
    })
    
    

def doctor_dashboard(request):

    # all appointments
    appointments = Appointment.objects.all()

    # total patients count
    patients = Patient.objects.count()

    # (optional) reports count - if model exists later
    reports = 0

    return render(request, 'doctor_dashboard.html', {
        'appointments': appointments,
        'patients': patients,
        'reports': reports
    })
    
@login_required(login_url='admin_login')
def admin_dashboard(request):

    print(request.user)
    print(request.user.groups.all())

    context = {
        'doctor_count': Doctor.objects.count(),
        'patient_count': Patient.objects.count(),
        'staff_count': Staff.objects.count(),
        'appointment_count': Appointment.objects.count(),
        'recent_patients': Patient.objects.order_by(
            '-patient_id'
        )[:5]
    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )
    
 
@login_required
def staff_dashboard(request):

    doctors_count = Doctor.objects.count()
    patients_count = Patient.objects.count()
    appointments_count = Appointment.objects.count()

    # 🔥 FIXED PARTS
    departments_count = Department.objects.count()

    pending_appointments = Appointment.objects.filter(status="PENDING").count()

    completed_appointments = Appointment.objects.filter(status="COMPLETED").count()

    billing_count = Billing.objects.count()

    return render(request, "staff_dashboard.html", {
        "doctors_count": doctors_count,
        "patients_count": patients_count,
        "appointments_count": appointments_count,
        "departments_count": departments_count,
        "pending_appointments": pending_appointments,
        "completed_appointments": completed_appointments,
        "billing_count": billing_count
    })
# =====================================================================================================

@login_required
def book_appointment(request):
    patient = Patient.objects.get(username=request.user.username)

    form = AppointmentForm()

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.patient = patient   # 🔥 auto link
            obj.save()

            return redirect('patient_dashboard')

    return render(request, 'book_appointment.html', {'form': form})


def my_appointments(request):
    patient = get_object_or_404(Patient, username=request.user.username)

    appointments = Appointment.objects.filter(patient=patient)

    return render(request, "my_appointment.html", {
        "appointments": appointments
    })

def update_appointment(request, id):
    appointment = Appointment.objects.get(appointment_id=id)  # ✅ correct

    if request.method == "POST":
        form = StaffAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = "SCHEDULED"
            appointment.save()
            return redirect('staff_appointments')
    else:
        form = StaffAppointmentForm(instance=appointment)

    return render(request, 'update_appointment.html', {'form': form})


@login_required
def doctor_appointments(request):
    doctor = Doctor.objects.get(username=request.user.username)

    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, 'doctor_appointments.html', {
        'appointments': appointments
    })
    
@login_required
def staff_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'staff_appointments.html', {'appointments': appointments})


# ========================================================================================
def add_prescription(request, appointment_id):

    appointment = Appointment.objects.get(
        appointment_id=appointment_id
    )

    doctor = Doctor.objects.get(
        username=request.user.username
    )

    if request.method == "POST":

        form = PrescriptionForm(request.POST)

        if form.is_valid():

            obj = form.save(commit=False)

            # Link doctor and appointment
            obj.doctor = doctor
            obj.appointment = appointment

            # Save prescription
            obj.save()

            # Go to add medicine page
            return redirect(
                'add_medicine',
                prescription_id=obj.prescription_id
            )

        else:
            print(form.errors)

    else:
        form = PrescriptionForm()

    return render(
        request,
        'add_prescription.html',
        {'form': form}
    )
    
    
def patient_prescriptions(request):
    if not request.user.groups.filter(name='Patient').exists():
        return redirect('login')

    patient = Patient.objects.get(username=request.user.username)

    prescriptions = Prescription.objects.filter(patient=patient)

    return render(request, 'patient_prescriptions.html', {
        'prescriptions': prescriptions
    })
    
    
def doctor_prescriptions(request):
    if not request.user.groups.filter(name='Doctor').exists():
        return redirect('login')

    doctor = Doctor.objects.get(username=request.user.username)

    prescriptions = Prescription.objects.filter(doctor=doctor)

    return render(request, 'doctor_prescriptions.html', {
        'prescriptions': prescriptions
    })
    

def delete_prescription(request, prescription_id):
    if not request.user.groups.filter(name='Doctor').exists():
        return redirect('login')

    doctor = Doctor.objects.get(username=request.user.username)

    prescription = get_object_or_404(Prescription, prescription_id=prescription_id, doctor=doctor)
    
    if request.method == "POST":
        prescription.delete()
    
    return redirect('doctor_prescriptions') # un list page name
    
# ========================================================================================

def add_medicine(request, prescription_id):
    prescription = Prescription.objects.get(prescription_id=prescription_id)

    form = MedicineForm()

    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.prescription = prescription
            obj.save()

            return redirect('add_medicine', prescription_id=prescription_id)

    return render(request, 'add_medicine.html', {
        'form': form,
        'prescription': prescription
    })


def view_medicines(request, prescription_id):
    prescription = Prescription.objects.get(prescription_id=prescription_id)
    medicines = Medicine.objects.filter(prescription=prescription)

    return render(request, 'view_medicines.html', {
        'medicines': medicines,
        'prescription': prescription
    })



# ===========================================================================================
@login_required
def create_bill(request, prescription_id):

    prescription = Prescription.objects.get(prescription_id=prescription_id)

    medicines = Medicine.objects.filter(prescription=prescription)

    total = sum(m.price for m in medicines)

    if request.method == "POST":

        payment_status = request.POST.get('payment_status')
        payment_method = request.POST.get('payment_method')

        Billing.objects.create(
            patient=prescription.patient,
            appointment=prescription.appointment,
            total_amount=total,
            payment_status=payment_status,
            payment_method=payment_method
        )

        return redirect('billing')

    return render(request, 'create_billing.html', {
        'prescription': prescription,
        'medicines': medicines,
        'total': total
    })


@login_required
def view_bills(request):

    bills = Billing.objects.all().order_by('-bill_date')

    return render(request, 'view_bills.html', {'bills': bills})


# ==================================================================================

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})

def staff_list(request):
    staffs = Staff.objects.all()
    return render(request, 'staff_list.html', {'staffs': staffs})


# ===================================================================================

def update_patient(request, id):
    patient = Patient.objects.get(patient_id=id)

    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'update_patient.html', {'form': form})


def delete_patient(request, id):
    patient = Patient.objects.get(patient_id=id)

    if request.method == "POST":
        patient.delete()
        return redirect('patient_list')

    return render(request, 'delete_patient.html', {'patient': patient})

# =======================================================================================


def update_doctor(request, id):
    doctor = get_object_or_404(Doctor, doctor_id=id)

    if request.method == "POST":
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'update_doctor.html', {'form': form})


def delete_doctor(request, id):
    doctor = get_object_or_404(Doctor, doctor_id=id)

    if request.method == "POST":
        doctor.delete()
        return redirect('doctor_list')

    return render(request, 'delete_doctor.html', {'doctor': doctor})

# ==========================================================================================


def update_staff(request, id):
    staff = get_object_or_404(Staff, staff_id=id)

    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm(instance=staff)

    return render(request, 'update_staff.html', {'form': form})

def delete_staff(request, id):
    staff = get_object_or_404(Staff, staff_id=id)

    if request.method == "POST":
        staff.delete()
        return redirect('staff_list')

    return render(request, 'delete_staff.html', {'staff': staff})

# ============================================================================================

def update_department(request, id):
    dept = get_object_or_404(Department, department_id=id)

    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=dept)

    return render(request, "update_department.html", {"form": form})


def delete_department(request, id):
    dept = get_object_or_404(Department, department_id=id)

    if request.method == "POST":
        dept.delete()
        return redirect('department_list')

    return render(request, "delete_department.html", {"dept": dept})



def logout_view(request):
    logout(request)
    return redirect('home')




    
    
