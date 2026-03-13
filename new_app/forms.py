from django import forms
from django.contrib.auth.forms import UserCreationForm
from new_app.models import Doctor, Register, Patient, Schedule, Booking, Review

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Register
        fields = ['username','password']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        exclude = ('reg_user',)

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ('reg_user',)

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['doctor', 'date', 'start_time', 'end_time', 'max_tokens']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'max_tokens': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 30'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ('patient', 'status')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} Stars") for i in range(5, 0, -1)], attrs={
                'class': 'form-select rounded-3'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 4,
                'placeholder': 'How was your experience with this doctor?'
            }),
        }
