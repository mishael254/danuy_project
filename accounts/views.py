from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from admindash.models import Client, Writer, Editor

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
       
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        messages.success(request,'You are now logged out')
        return redirect('index')
    

def register(request):
    if request.method=="POST":
        #Get form values
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        
        #check if password match
        if password == password2:
            #Check Username
            if User.objects.filter(username=username).exists():
                messages.error(request,'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'That email is being used')
                    return redirect('register')
                else:
                    #Looks good
                    user=User.objects.create_user(username=username,password=password,email=email,
                    first_name=first_name,last_name=last_name)
                    # Login after register
                    # auth.login(request,user)
                    # messages.success(request,'You are now logged in')
                    # return redirect('index')
                    user.save()
                    client = Client.objects.create(client=user)
                    messages.success(request,'You are now registered and can login')
                    return redirect('login')

        else:
            messages.error(request,'Password do not match')
            return redirect('register')
    else:
        return render(request,'accounts/register.html')
        

def nursinglogin(request):
    if request.method=="POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            messages.error(request, 'Please log in')
            return redirect('nursinglogin')
       
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            return redirect('Dashboard')
        else:
            messages.error(request,'Please log in')
            return redirect('nursinglogin')
    else:
        return render(request,'accounts/nursinglogin.html')


def nursinglogout(request):
    if request.method=='POST':
        auth.logout(request)
        messages.success(request,'You are now logged out')
    return redirect('home')
    

def nursingregister(request):
    if request.method == "POST":
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if password match
        if password == password2:
            # Check Username and Email
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('nursingregister')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'That email is being used')
                return redirect('nursingregister')
            else:
                # Create User and Client
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                client = Client.objects.create(client=user)

                messages.success(request, 'You are now registered and can login')
                return redirect('nursinglogin')

        else:
            messages.error(request, 'Password do not match')
            return redirect('nursingregister')
    else:
        return render(request, 'accounts/nursingregister.html')

# views.py
def writerslogin(request):
    if request.method=="POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            messages.error(request, 'Please log in')
            return redirect('writerslogin')
       
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                writer = user.freelancers
                auth.login(request, user)
                messages.success(request,'You are now logged in as a Writer')
                return redirect('writerdashboard')
            except Writer.DoesNotExist:
                pass
            
            try:
                editor = user.editor
                auth.login(request, user)
                messages.success(request,'You are now logged in as an Editor/Admin')
                return redirect('admindashboard')
            except Editor.DoesNotExist:
                pass
            
            messages.error(request, 'Invalid Login Credentials')
            return redirect('writerslogin')
        else:
            messages.error(request,'Invalid Login Credentials')
            return redirect('writerslogin')
    else:
        return render(request,'accounts/writerslogin.html')



def writerslogout(request):
    if request.method=='POST':
        auth.logout(request)
        messages.success(request,'You are now logged out')
    return redirect('writerslogin')


def writersregister(request):
    if request.method == "POST":
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if password match
        if password == password2:
            # Check Username and Email
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('writersregister')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'That email is being used')
                return redirect('writersregister')
            else:
                # Create User and Client
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                writer = Writer.objects.create(writer=user)

                messages.success(request, 'You are now registered and can login')
                return redirect('writerslogin')

        else:
            messages.error(request, 'Password do not match')
            return redirect('writersregister')
    else:
        return render(request, 'accounts/writersregister.html')

