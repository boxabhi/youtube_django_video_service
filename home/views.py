from django.shortcuts import render,redirect
from .models import *
import stripe
from datetime import datetime, timedelta
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    course = Course.objects.all()
    context = {'course': course}
    
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        request.session['profile'] = profile.is_pro
    
    print(context)
    return render(request, 'home.html' , context)

def view_course(request,slug):
    course = Course.objects.filter(slug =slug).first()
    course_modules = CourseModule.objects.filter(course=course)
    context = {'course':course , 'course_modules':course_modules}
    return render(request, 'course.html' , context)

@login_required(login_url='/login/')
def become_pro(request):
    if request.method == 'POST':
        membership = request.POST.get('membership' , 'MONTHLY')
        amount = 1000
        if membership == 'YEARLY':
            amount = 11000
        stripe.api_key = 'sk_test_qu7ivgHp9WRHlHJjs2QHugIA00hKFbC5qc'

        customer = stripe.Customer.create(
            email = "abhijeetg40@gmail.com",
			name=request.user.username,
            source=request.POST['stripeToken']
			)
            
        charge = stripe.Charge.create(
			customer=customer,
			amount=amount*100,
			currency='inr',
			description="Membership",   
		)
        
        print(charge['amount'])
        if charge['paid'] == True:
            profile = Profile.objects.filter(user = request.user).first()
            if charge['amount'] == 100000:
                profile.subscription_type = 'M'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(30)
                profile.pro_expiry_date = expiry
                profile.save()
                
            elif charge['amount'] == 1100000:
                profile.subscription_type = 'Y'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(365)
                profile.pro_expiry_date = expiry
                profile.save()
        
        print(charge)
        return redirect('/charge/')
   
    return render(request, 'become_pro.html')

def charge(request):
    return render(request, 'charge.html')



def login_attempt(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username).first()
        
        if user is None:
            context = {'message' : 'No user found' , 'class' : 'danger'}
            return render(request,'login.html' , context)
        else:
            user = authenticate(username = username , password = password)
            print(user)
            if user is None:
                context = {'message' : 'Invalid credentials' , 'class' : 'danger'}
                return render(request,'login.html' , context)
            else:
                login(request , user)
                return redirect('home')            
    return render(request,'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(email=email)
        if user:
            context = {'message' : 'User already exists' , 'class' : 'danger'}
            return render(request,'register.html' , context)
        else :
            context = {'message' : 'User created successfully' , 'class' : 'success'}
            user = User(username = username)
            user.set_password(password)
            user.save()
            return render(request,'register.html' , context)
        
    return render(request,'register.html')



def logout_attempt(request):
    request.session.profile = None
    logout(request)
    return redirect('/')
    