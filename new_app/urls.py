from django.urls import path
from new_app import views, doctor_views, patient_views, admin_views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='logout_view'),



    # Admin URLS

    path('admin-dashboard/', admin_views.admin_viewbase, name='admin_viewbase'),
    path('add-doctor/', admin_views.add_doctor, name='add_doctor'),
    path('doctor-list/', admin_views.doctor_view, name='doctor_view'),
    path('patient-list/', admin_views.admin_viewpatient, name='admin_viewpatient'),
    path('delete-doctor/<int:id>/', admin_views.delete_doctor, name='delete_doctor'),
    path('add-schedule/', admin_views.add_schedule, name='add_schedule'),
    path('view-schedule/', admin_views.view_schedule, name='view_schedule'),
    path('view-reviews/', admin_views.view_review, name='view_review'),
    path('reply-review/<int:id>/', admin_views.reply_review, name='reply_review'),
    path('admin-bookings/', admin_views.admin_view_bookings, name='admin_view_bookings'),
    path('update-booking-status/<int:id>/<str:status>/', admin_views.update_booking_status, name='update_booking_status'),





    # Doctor URLS

    path('doctor-add/', doctor_views.doctor_add, name='doctor_add'),
    path('doctor-home/', doctor_views.doctor_viewbase, name='doctor_viewbase'),
    path('doctor/profile-update/', doctor_views.doctor_profile_update, name='doctor_profile_update'),
    path('doctor/view-bookings/', doctor_views.doctor_view_bookings, name='doctor_view_bookings'),
    path('doctor/update-status/<int:pk>/<str:status>/', doctor_views.update_status, name='update_status'),
    path('doctor/view-schedule/', doctor_views.doctor_view_schedule, name='doctor_view_schedule'),
    path('doctor/view-reviews/', doctor_views.doctor_view_reviews, name='doctor_view_reviews'),





    # Patient URLS

    path('patient-register/', patient_views.patient_add, name='patient_add'),
    path('patient-home/', patient_views.patient_viewbase, name='patient_viewbase'),
    path('patient-profile/', patient_views.patient_profile_view, name='patient_profile_view'),
    path('patient-profile-edit/', patient_views.edit_patient_profile, name='edit_patient_profile'),
    path('patient-view-doctors/', patient_views.patient_view_doctors, name='patient_view_doctors'),
    path('patient-view-schedules/', patient_views.patient_view_schedules, name='patient_view_schedules'),
    path('add-booking/', patient_views.add_booking, name='add_booking'),
    path('booking-history/', patient_views.patient_booking_history, name='patient_view_bookings'),
    path('add-review/<int:doctor_id>/', patient_views.add_review, name='add_review'),
    path('my-reviews/', patient_views.view_my_reviews, name='view_my_reviews'),

]
