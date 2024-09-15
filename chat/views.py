from django.shortcuts import render
from .models import Message
from .models import Chat
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'],chat= myChat, author=request.user, receiver=request.user)
    chatMessages = Message.objects.filter(chat__id = 1)
    return render(request, 'chat/index.html', {'messages': chatMessages})



def login_view(request):
    redirect = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})

def signup_view(request):
    message = request.GET.get('message', 'Mina sagt')
    print("message: " + message)
    state = {
        'user': "User is already taken",
        'pass': "Passwords don't match",
        'email': "Email is already registered"
        }
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Check if the two passwords match
        if password != password2:
            return render(request, 'auth/signup.html', {'message': state['pass']})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'auth/signup.html', {'message': state['user']})
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'auth/signup.html', {'message': state['email']})

        User.objects.create_user(username=username, password=password, email=email)
    return render(request, 'auth/signup.html')