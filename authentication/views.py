from telnetlib import LOGOUT
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from gfg import settings
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username = username):
            messages.error(request, "Username already exist Please try some other username")
            return redirect('home')
        if User.objects.filter(email= email):
            messages.error(request, 'Email already exists')
            return redirect('home')
        
        if len(username)>10:
            messages.error(request,"username must be under 10 character")
        
        if pass1 != pass2:
            messages.error(request, "Passwords are not same")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-numeric!")
            return redirect('home')
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been successfully created. We have sent you a confiration email, please confirm your account")
        
        #Welcome email
        subject = "welcome to GfG-Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to gfg!! \n Thank your for visiting us \n we have s ent you confirmation mail, please confirm your email address \n\n Thanking You"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email, to_list, fail_silently = True)
        return redirect('signin')
    
    
    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username = username, password = pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, "authentication/index.html",{'fname':fname})
        else:
            messages.error(request, "Bad credentials")
            return redirect('home')
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "logged Out Successfully")
    return redirect('home')

def portal(request):
    return render(request, "authentication/portal.html")

def contact(request):
    return render(request, "authentication/contact.html")