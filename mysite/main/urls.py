from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path('', views.login_request, name='login_request'),
    path('homepage/', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('new_task/', views.new_task, name='new_task'),
    path('logout_request/', views.logout_request, name='logout_request'),
    path('change_password/', views.change_password, name='change_password'),
    path('edit_task/<pk>', views.edit_task, name='edit_task'),
    path('delete_task/<pk>', views.delete_task, name='delete_task'),
    path('pdf_download/<pk>', views.pdf_download, name='pdf_download'),
    path('mail_task/<pk>', views.mail_task, name='mail_task'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='main/password-reset/password_reset.html',
             subject_template_name='main/password-reset/password_reset_subject.txt',
             email_template_name='main/password-reset/password_reset_email.html',
             success_url='done'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='main/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='main/password-reset/password_reset_confirm.html',
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='main/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),


]