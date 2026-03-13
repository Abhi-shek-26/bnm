from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from new_app.forms import LoginForm


def Login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect('admin_viewbase')

            elif user.is_doctor:
                return redirect('doctor_viewbase')

            elif user.is_patient:
                return redirect('patient_viewbase')


        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')
def landing_page(request):
    return render(request, 'landing_page.html')




def Logout(request):
    logout(request)
    return redirect('landing_page')