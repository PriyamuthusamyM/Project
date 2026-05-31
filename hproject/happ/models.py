from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    dob = models.DateField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    blood_group = models.CharField(max_length=5)

    def __str__(self):
        return self.name
    
    
class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name
    
    
class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_name = models.CharField(max_length=100)

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff_name
    
# ============================================================================================================================
    
    
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    appointment_id = models.AutoField(primary_key=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    reason = models.TextField()

    # Staff will assign these
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)
    
    

    def __str__(self):
        return f"{self.patient.name} - {self.status}"
    
    
# ===================================================================================


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medicine_details = models.TextField()
    notes = models.TextField()
    prescription_date = models.DateField()
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)  # 🔥 ADD THIS

    def __str__(self):
        return f"Prescription {self.prescription_id}"
    
    
# ===================================================================================

class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    medicine_name = models.CharField(max_length=100)

    dosage = models.CharField(max_length=50)  # 1 tablet, 5ml
    timing = models.CharField(max_length=100) # morning/night
    days = models.IntegerField()  # how many days
    price = models.FloatField()

    def __str__(self):
        return self.medicine_name
    
    
# ===================================================================================

class Billing(models.Model): 
    bill_id = models.AutoField(primary_key=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('PAID', 'Paid'),
            ('PENDING', 'Pending')
        ],
        default='PENDING'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('CASH', 'Cash'),
            ('CARD', 'Card'),
            ('UPI', 'UPI')
        ],
        null=True,
        blank=True
    )

    bill_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill {self.bill_id} - {self.patient.name}"
    
    
# ==============================================================================================


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)