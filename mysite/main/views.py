from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from .forms import PostForm, UserCreateForm
from django.contrib import messages
from django.contrib.auth.models import User
from reportlab.pdfgen import canvas 
import re
from django.core.mail import EmailMultiAlternatives

# Create your views here.

def homepage(request):
    tasks = Task.objects.filter(author=request.user)
    return render(request, 'main/task_list.html', {'tasks':tasks})

def register(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            if User.objects.filter(email=form.cleaned_data.get('email')).count()==2:
                messages.error(request, "Email Already registered")
                user.delete()
                return redirect('/register', target='_blank')
            else :
                username = form.cleaned_data.get('username')
                messages.success(request, f"New account created: {username}")
                login(request, user)
                return redirect('/homepage', target='_blank')
        else :
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            if (password1!=password2):
                messages.error(request, "Password Doesn't match")
            elif User.objects.filter(email=form.cleaned_data.get('email')).exists():
                messages.error(request, "Email Already registered")
            else :
                messages.error(request, "Username already exists")
            return redirect('/register', target='_blank')
    form = UserCreateForm()
    return render(request, 'main/register.html', {"form":form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/homepage')
            else:
                messages.info(request, "Invalid username or password.")
                return redirect('/')
        else:
            messages.info(request, "Invalid username or password.")
            return redirect('/')
    form = AuthenticationForm()
    return render(request, 'main/login.html', {"form":form})

def new_task(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return redirect('/homepage')
    else:
        form = PostForm()
    return render(request, 'main/new_task.html', {'form': form})

def edit_task(request, pk):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            task = get_object_or_404(Task, pk=pk)
            task.delete()
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return redirect('/homepage')
    task = get_object_or_404(Task, pk=pk)
    form=PostForm()
    form.fields['task_title'].initial = task.task_title
    form.fields['task_content'].initial = task.task_content
    return render(request, 'main/new_task.html', {'form': form})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('/homepage')

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully')
            return redirect('/homepage')
        else:
            messages.error(request, 'Please correct the error.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/change_password.html', {'form': form})

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def mail_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    subject, from_email, to = task.task_title, 'pareshchauhan501@gmail.com', request.user.email
    text_content = cleanhtml(task.task_content)
    html_content = task.task_content
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    messages.success(request, 'Mail has been sent')
    return redirect('/homepage')

def pdf_download(request, pk):
    task = get_object_or_404(Task, pk=pk)   
    response = HttpResponse(content_type='application/pdf')  
    response['Content-Disposition'] = 'inline; filename="task.pdf"'  
    p = canvas.Canvas(response)  
    p.setFont("Times-Roman", 55)
    p.drawString(100,700, task.task_title)
    p.line(0, 780, 1000, 778)
    p.setFont("Times-Roman", 20)
    p.drawString(10 ,650, cleanhtml(task.task_content))
    p.showPage()  
    p.save()  
    return response