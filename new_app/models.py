from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Register(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)


class Doctor(models.Model):
    reg_user = models.OneToOneField(Register, on_delete=models.CASCADE, related_name='doctor_profile')
    doctor_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to='doctors/')

    def __str__(self):
        return self.doctor_name

class Patient(models.Model):
    reg_user = models.OneToOneField(Register, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    address =  models.CharField(max_length=100)

    blood_group = models.CharField(max_length=10, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_tokens = models.IntegerField(default=20)

    def get_booking_count(self):
        return self.booking_set.count()

    def get_availability_percentage(self):
        if self.max_tokens > 0:
            return (self.get_booking_count() / self.max_tokens) * 100
        return 0

    def __str__(self):
        return f"{self.doctor.doctor_name} - {self.date}"


class Booking(models.Model):
    STATUS_CHOICES =(
    ('pending' , 'Pending'),
    ('Approved' , 'Approved'),
    ('Rejected' , 'Rejected'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.patient} - {self.doctor.doctor_name}"


from django.db import models

class Review(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    reply = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.doctor.doctor_name} by {self.patient}"