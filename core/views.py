from django.shortcuts import render
from .models import Destination

def home(request):
    destinations = Destination.objects.all()
    context = {
        'destinations': destinations
    }
    return render(request, 'core/home.html', context)

