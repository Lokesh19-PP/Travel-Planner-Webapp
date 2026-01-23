from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Destination

def home(request):
    query = request.GET.get('search', '')  # Get search term from URL
    if query:
        destinations = Destination.objects.filter(name__icontains=query)
    else:
        destinations = Destination.objects.all()
    return render(request, 'core/home.html', {'destinations': destinations, 'query': query})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'core/login.html')

