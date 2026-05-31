from django import forms
from .models import Patient, Doctor, Staff,Department,Appointment,Prescription,Medicine,Billing
from django.contrib.auth.models import User

class AdminSigupForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'password'
        ]

        widgets = {
            'password': forms.PasswordInput()
        }

# ================= PATIENT FORM =================
class PatientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = '__all__'


# ================= DOCTOR FORM =================
class DoctorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = '__all__'


# ================= STAFF FORM =================
class StaffForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Staff
        fields = '__all__'
        
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']
        widgets = {
            'department_name': forms.TextInput(attrs={
                'placeholder': 'Enter Department Name'
            })
        }
        
# ==================================================================================

# Patient form
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['reason']
# Staff form
class StaffAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time']
        
        
# ============================================================================================


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medicine_details', 'notes', 'prescription_date']


# =================================================================================================

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'dosage', 'timing', 'days', 'price']
        
        
# ===================================================================================================

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['patient', 'appointment', 'total_amount', 'payment_status', 'payment_method']
        
        
#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


