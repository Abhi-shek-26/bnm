from django.contrib import admin

from new_app.models import Register, Doctor, Patient, Schedule, Booking, Review

# Register your models here.

admin.site.register(Register)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Schedule)
admin.site.register(Booking)
admin.site.register(Review)
