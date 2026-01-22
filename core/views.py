from django.shortcuts import render
from .models import Destination

def home(request):
    query = request.GET.get('search', '')  # Get search term from URL
    if query:
        destinations = Destination.objects.filter(name__icontains=query)
    else:
        destinations = Destination.objects.all()
    return render(request, 'core/home.html', {'destinations': destinations, 'query': query})


