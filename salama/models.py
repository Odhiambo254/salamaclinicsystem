from wsgiref.validate import validator

from django.db import models

# Create your models here.
class Admin(models.Model):
    username=models.CharField(max_length=50 ,unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.username



class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)
    address=models.CharField(max_length=50 , default="uknown" )
    id_number=models.CharField(max_length=11, unique=True , null=True)
    next_of_kin=models.CharField(max_length=50 , null=True)

    inpatient_number = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.inpatient_number}"

class Appointment(models.Model):
        patient = models.ForeignKey('Patient',  on_delete=models.CASCADE)
        appointment_date = models.DateTimeField()
        status = models.CharField(max_length=20, choices=[('booked', 'Booked'), ('completed', 'Completed')],
                                  default='booked')
        def __str__(self):
            return f"Appointment for {self.patient.first_name} {self.patient.last_name} on {self.appointment_date}"



#billing model
class Billing(models.Model):
    patient=models.ForeignKey('Patient', on_delete=models.CASCADE)
    appointment=models.ForeignKey('Appointment', on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now_add=True)
    amount_due=models.DecimalField(max_digits=10,decimal_places=2)
    amount_paid=models.DecimalField(max_digits=10,decimal_places=2)
    date_updated=models.DateTimeField(auto_now=True)
    payment_status=models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'),('Paid', 'Paid')],
        default='Pending'
    )
    def balance_due(self):
        return self.amount_due -self.amount_paid
    def __str__(self):
        return f'Billing for {self.patient.first_name} {self.patient.last_name}'

