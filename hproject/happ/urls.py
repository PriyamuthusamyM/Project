from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    
   
    path('home', views.home, name='home'), 
    path('aboutus', views.aboutus, name='aboutus'),
    path('contactus', views.contactus, name='contactus'),
    path('feedback-list', views.feedback_list, name='feedback_list'),
    
    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),
    path('staffclick', views.staffclick_view),
    
    path('admin_login', views.admin_login,name='admin_login'),
    path('doctor_login', views.doctor_login,name='doctor_login'),
    path('patient_login', views.patient_login,name='patient_login'),
    path('staff_login', views.staff_login, name='staff_login'),
    
    

    path('adminsignup', views.admin_signup, name='adminsignup'),
    path('patient_signup',views.patient_signup,name='patient_signup'),
    path('doctor_signup',views.doctor_signup,name='doctor_signup'),
    path('staff_signup',views.staff_signup,name='staff_signup'),
    
    path('add_department',views.add_department,name='add_department'),
    

   
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('patient_dashboard', views.patient_dashboard, name="patient_dashboard"),
    path('doctor_dashboard', views.doctor_dashboard, name="doctor_dashboard"),
    path('staff_dashboard', views.staff_dashboard, name="staff_dashboard"),
    
    # ====================================================================================================
    
    # Patient
    path('patient/book-appointment/', views.book_appointment, name='book_appointment'),
    path('patient/<int:patient_id>/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('my-appointments/', views.my_appointments, name='my-appointments'),

    # Staff
    path('staff/appointments/', views.staff_appointments, name='staff_appointments'),
    path('staff/update/<int:id>/', views.update_appointment, name='update_appointment'),

    # Doctor
    path('doctor_appointments/', views.doctor_appointments, name='doctor_appointments'),
   
#    ==================================================================================================
    # Prescription
    path('doctor/add-prescription/<int:appointment_id>/', views.add_prescription, name='add_prescription'),
    path('patient/prescriptions/', views.patient_prescriptions, name='patient_prescriptions'),
    path('doctor/prescriptions/', views.doctor_prescriptions, name='doctor_prescriptions'),
    path('delete-prescription/<int:prescription_id>/', views.delete_prescription, name='delete_prescription'),
    
    # ===============================================================================================
    # Medicine
    path('add_medicine/<int:prescription_id>/', views.add_medicine, name='add_medicine'),
    path('view_medicines/<int:prescription_id>/', views.view_medicines, name='view_medicines'),
    
    # ==================================================================================================
    
    # Billing
    path('create_bill/<int:prescription_id>/', views.create_bill, name='create_bill'),
    path('billing/', views.view_bills, name='billing'),
    
            
    # ==================================================================================================
    
    path('patient_list/', views.patient_list, name='patient_list'),
    path('patient/update/<int:id>/', views.update_patient, name='update_patient'),
    path('patient/delete/<int:id>/', views.delete_patient, name='delete_patient'),
    
    
    path('doctor_list/', views.doctor_list, name='doctor_list'),        
    path('doctor/update/<int:id>/', views.update_doctor, name='update_doctor'),
    path('doctor/delete/<int:id>/', views.delete_doctor, name='delete_doctor'),
    
    
    path('staff_list/', views.staff_list, name='staff_list'),
    path('staff/update/<int:id>/', views.update_staff, name='update_staff'),
    path('staff/delete/<int:id>/', views.delete_staff, name='delete_staff'),
    
    path('department_list/', views.view_department, name='department_list'),
    path('department/update/<int:id>/', views.update_department, name='update_department'),
    path('department/delete/<int:id>/', views.delete_department, name='delete_department'),
    
    
    path('logout', views.logout_view, name='logout'),
        
]

