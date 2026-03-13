
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.utils import timezone

from .forms import LoginForm, DoctorForm, ScheduleForm
from .models import Doctor, Schedule, Review, Booking, Patient


def admin_viewbase(request):
    total_patients = Patient.objects.count()
    active_doctors = Doctor.objects.count()
    bookings_today = Booking.objects.all().count()
    recent_doctors = Doctor.objects.all().order_by('-id')[:5]
    patients_list = Patient.objects.all().order_by('-id')

    context = {
        'patient_count': total_patients,
        'doctor_count': active_doctors,
        'booking_count': bookings_today,
        'recent_doctors': recent_doctors,
        'patients': patients_list,
    }
    return render(request, 'admin/admin_viewbase.html', context)
def add_doctor(request):
    login_form = LoginForm()
    doctor_form = DoctorForm()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        doctor_form = DoctorForm(request.POST,request.FILES)

        if login_form.is_valid() and doctor_form.is_valid():
            try:
                with transaction.atomic():
                    user = login_form.save(commit=False)
                    raw_password = login_form.cleaned_data.get('password')
                    user.set_password(raw_password)
                    user.is_doctor = True
                    user.save()

                    doctor_profile = doctor_form.save(commit=False)
                    doctor_profile.reg_user = user
                    doctor_profile.save()
                return redirect('admin_viewbase')
            except Exception as e:
                print(f"Transaction Error: {e}")
        else:
            print("Login Form Errors:", login_form.errors)
            print("Doctor Form Errors:", doctor_form.errors)

    return render(request, 'admin/add_doctor.html', {
        'login_form': login_form,
        'doctor_form': doctor_form
    })


def admin_viewpatient(request):

    patients = Patient.objects.all().order_by('-id')

    return render(request, 'admin/admin_viewpatient.html', {
        'patients': patients
    })


def doctor_view(request):
    data = Doctor.objects.all()
    return render(request, 'admin/doctor_view.html', {'data': data})

def delete_doctor(request,id):
   data = Doctor.objects.get(id=id)
   data.delete()
   return redirect('doctor_view')


def add_schedule(request):
    Schedule.objects.filter(date__lt=timezone.now().date()).delete()

    form = ScheduleForm()
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.rege_user = request.user
            schedule.save()
            return redirect('doctor_view')

    return render(request, 'admin/add_schedule.html', {'form': form})


def view_schedule(request):
    Schedule.objects.filter(date__lt=timezone.now().date()).delete()
    data = Schedule.objects.all().order_by('date')

    return render(request, 'admin/view_schedule.html', {'data': data})

def view_review(request):
    if request.user.is_authenticated and hasattr(request.user, 'is_doctor') and request.user.is_doctor:
        reviews = Review.objects.filter(doctor__reg_user=request.user)
    else:
        reviews = Review.objects.all()
    return render(request, 'admin/view_review.html', {'reviews': reviews})


def reply_review(request, id):

    review = get_object_or_404(Review, id=id)

    if request.method == 'POST':
        reply_text = request.POST.get('reply_text')
        review.reply = reply_text
        review.save()

        return redirect('view_review')

    return render(request, 'admin/reply_review.html', {'review': review})

def admin_view_bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')
    booking_count = bookings.count()

    return render(request, 'admin/admin_bookings.html', {
        'bookings': bookings,
        'count': booking_count
    })

def update_booking_status(request, id, status):
    booking = Booking.objects.get(id=id)
    booking.status = status
    booking.save()
    return redirect('admin_view_bookings')


