
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404

from .forms import LoginForm, DoctorForm
from .models import Review, Schedule, Booking, Doctor


def doctor_add(request):
    login_form = LoginForm()
    doctor_form = DoctorForm()

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        doctor_form = DoctorForm(request.POST)

        if login_form.is_valid() and doctor_form.is_valid():
            with transaction.atomic():
                user = login_form.save(commit=False)
                user.is_doctor = True
                user.save()

                doctor_profile = doctor_form.save(commit=False)
                doctor_profile.reg_user = user
                doctor_profile.save()
            return redirect('doctor_view')

    return render(request, 'add_doctor.html', {
        'login_form': login_form,
        'doctor_form': doctor_form
    })


def get_doctor_profile(user):
    return get_object_or_404(Doctor, reg_user=user)


@login_required
def doctor_viewbase(request):
    doctor = get_object_or_404(Doctor, reg_user=request.user)


    today_slots_count = Schedule.objects.filter(doctor=doctor).count()

    total_bookings = Booking.objects.filter(schedule__doctor=doctor).count()

    unique_patients_count = Booking.objects.filter(schedule__doctor=doctor).values('patient').distinct().count()

    upcoming_appointments = Booking.objects.filter(
        schedule__doctor=doctor
    ).order_by('-id')[:5]

    return render(request, 'doctor/index.html', {
        'doctor': doctor,
        'today_slots_count': today_slots_count,
        'unique_patients_count': unique_patients_count,
        'total_bookings': total_bookings,
        'upcoming_appointments': upcoming_appointments,
    })


@login_required(login_url='login_view')
def doctor_profile_update(request):
    doctor = get_object_or_404(Doctor, reg_user=request.user)
    form = DoctorForm(instance=doctor)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_profile_update')
    return render(request, 'doctor/'
                           'doctor_profile.html', {'form': form, 'doctor': doctor})

@login_required(login_url='login_view')
def doctor_view_bookings(request):
    bookings = Booking.objects.filter(doctor__reg_user=request.user).order_by('-created_at')
    return render(request, 'doctor/doctor_bookings.html', {'bookings': bookings})

@login_required(login_url='login_view')
def update_status(request, pk, status):
    booking = get_object_or_404(Booking, id=pk, doctor__reg_user=request.user)
    booking.status = status
    booking.save()
    return redirect('doctor_view_bookings')


@login_required(login_url='login_view')
def doctor_view_schedule(request):

    doctor_profile = get_object_or_404(Doctor, reg_user=request.user)


    schedules = Schedule.objects.filter(doctor=doctor_profile).order_by('date', 'start_time')

    return render(request, 'doctor/doctor_schedule.html', {'schedules': schedules})

@login_required(login_url='login_view')
def doctor_view_reviews(request):
    reviews = Review.objects.filter(doctor__reg_user=request.user)
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        reply_text = request.POST.get('reply')
        review = get_object_or_404(Review, id=review_id, doctor__reg_user=request.user)
        review.reply = reply_text
        review.save()
        return redirect('doctor_view_reviews')
    return render(request, 'doctor/doctor_reviews.html', {'reviews': reviews})
