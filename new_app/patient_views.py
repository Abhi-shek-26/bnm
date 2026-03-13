from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from new_app.forms import LoginForm, PatientForm, BookingForm, ReviewForm
from new_app.models import Patient, Doctor, Schedule, Booking, Review



def patient_add(request):

    if request.method == 'POST':

        login_form = LoginForm(request.POST)
        patient_form = PatientForm(request.POST)

        if login_form.is_valid() and patient_form.is_valid():

            user = login_form.save(commit=False)

            user.set_password(login_form.cleaned_data['password'])

            user.is_patient = True

            user.save()

            patient = patient_form.save(commit=False)
            patient.reg_user = user
            patient.save()

            return redirect('Login')

    else:
        login_form = LoginForm()
        patient_form = PatientForm()

    return render(request, 'patient/patientReg.html', {
        'login_form': login_form,
        'patient_form': patient_form
    })


@login_required(login_url='login_view')
def patient_viewbase(request):
    latest_doctor = Doctor.objects.latest('id')

    return render(request, 'patient/index.html', {
        'latest_doctor': latest_doctor
    })




@login_required(login_url='login_view')
def patient_profile_view(request):

    patient_data = Patient.objects.get(reg_user=request.user)

    return render(request, 'patient/patient_profile.html', {
        'patient_data': patient_data
    })





@login_required(login_url='login_view')
def edit_patient_profile(request):

    patient_data = Patient.objects.get(reg_user=request.user)

    form = PatientForm(instance=patient_data)

    if request.method == 'POST':

        form = PatientForm(request.POST, instance=patient_data)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('patient_profile_view')

    return render(request, 'patient/patient_edit_profile.html', {
        'form': form,
        'patient_data': patient_data
    })


def add_booking(request):
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            schedule = form.cleaned_data.get('schedule')


            if schedule.get_booking_count() >= schedule.max_tokens:
                messages.error(request, "This time slot is fully booked.")
                return render(request, 'patient/add_booking.html', {'form': form})


            patient_profile, created = Patient.objects.get_or_create(
                reg_user=request.user,
                defaults={'name': request.user.username,
                          'age':0}
            )

            booking = form.save(commit=False)
            booking.patient = patient_profile
            booking.status = 'Pending'
            booking.save()

            messages.success(request, "Booking request sent successfully!")
            return redirect('patient_view_bookings')

    return render(request, 'patient/add_booking.html', {'form': form})



@login_required(login_url='login_view')
def patient_view_doctors(request):

    doctors = Doctor.objects.all()

    return render(request, 'patient/patient_view_doctors.html', {
        'doctors': doctors
    })




@login_required(login_url='login_view')
def patient_view_schedules(request):
    today = timezone.now().date()

    schedules = Schedule.objects.select_related('doctor').all().order_by('date')

    return render(request, 'patient/patient_view_schedules.html', {
        'schedules': schedules
    })



@login_required(login_url='login_view')
def patient_booking_history(request):

    patient = Patient.objects.get(reg_user=request.user)

    bookings = Booking.objects.filter(patient=patient).order_by('-created_at')

    return render(request, 'patient/booking_history.html', {
        'bookings': bookings
    })




@login_required(login_url='login_view')
def add_review(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    reviews = Review.objects.filter(doctor=doctor).order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.patient = Patient.objects.get(reg_user=request.user)
            review.doctor = doctor
            review.save()
            return redirect('add_review', doctor_id=doctor_id)
    else:
        form = ReviewForm()

    return render(request, 'patient/add_review.html', {
        'form': form,
        'doctor': doctor,
        'reviews': reviews
    })


@login_required(login_url='login_view')
def view_my_reviews(request):
    try:
        patient_profile = Patient.objects.get(reg_user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, "Patient profile not found.")
        return redirect('home')

    user_reviews = Review.objects.filter(patient=patient_profile).order_by('-created_at')

    return render(request, 'patient/my_reviews.html', {
        'reviews': user_reviews
    })