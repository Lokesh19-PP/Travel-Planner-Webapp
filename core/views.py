from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Itinerary, Destination
from django.shortcuts import get_object_or_404
from .forms import ItineraryForm
from .forms import ReviewForm
from django.db import models
from django.db.models import Avg

def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)

def custom_500(request):
    return render(request, 'core/500.html', status=500)

def home(request):
    query = request.GET.get('search', '')  # Get search term from URL
    if query:
        destinations = Destination.objects.filter(name__icontains=query)
    else:
        destinations = Destination.objects.all()[:3]
    return render(request, 'core/home.html', {'destinations': destinations, 'query': query})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()
        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "core/signup.html")

@login_required(login_url='login')
def profile_view(request):
    user = request.user
    return render(request, 'core/profile.html', {'user': user})

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    reviews = destination.reviews.all().order_by('-created_at')

    # Calculate average rating
    if reviews.exists():
        average_rating = round(reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'], 1)
    else:
        average_rating = 0  # Use 0 instead of None for easier star rendering

    return render(request, 'core/destination_detail.html', {
        'destination': destination,
        'reviews': reviews,
        'average_rating': average_rating,
    })




def destination_list(request):
    destinations = Destination.objects.all()

    # Filters
    country = request.GET.get('country')
    price = request.GET.get('price')
    rating = request.GET.get('rating')
    query = request.GET.get('search')  # search from home page

    if query:
        destinations = destinations.filter(name__icontains=query)

    if country and country != 'All':
        destinations = destinations.filter(country__iexact=country)
    if price and price != 'All':
        destinations = destinations.filter(price_range=price)
    if rating and rating != 'All':
        destinations = destinations.filter(rating__gte=float(rating))

    countries = Destination.objects.values_list('country', flat=True).distinct()
    price_ranges = ['$', '$$', '$$$']
    ratings = [4, 3, 2, 1]

    context = {
        'destinations': destinations,
        'countries': countries,
        'price_ranges': price_ranges,
        'ratings': ratings,
        'selected_country': country,
        'selected_price': price,
        'selected_rating': rating,
        'query': query,
    }
    return render(request, 'core/destination_list.html', context)

@login_required
def itinerary_list(request):
    itineraries = Itinerary.objects.filter(user=request.user)
    return render(request, 'core/itinerary_list.html', {'itineraries': itineraries})

@login_required
def itinerary_detail(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    return render(request, 'core/itinerary_detail.html', {'itinerary': itinerary})
@login_required
def itinerary_create(request):
    destination_id = request.GET.get('destination')
    destination = None
    if destination_id:
        destination = get_object_or_404(Destination, id=destination_id)

    user_itineraries = Itinerary.objects.filter(user=request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'add_existing':
            itinerary_id = request.POST.get('itinerary')
            itinerary = get_object_or_404(Itinerary, id=itinerary_id, user=request.user)
            if destination:
                itinerary.destinations.add(destination)
                messages.success(request, f'"{destination.name}" added to "{itinerary.name}"')
            return redirect('itinerary_list')
        else:
            form = ItineraryForm(request.POST)
            if form.is_valid():
                itinerary = form.save(commit=False)
                itinerary.user = request.user
                itinerary.save()
                form.save_m2m()
                messages.success(request, f'Itinerary "{itinerary.name}" created successfully!')
                return redirect('itinerary_list')
    else:
        form = ItineraryForm(initial={'destinations': [destination]} if destination else None)

    return render(request, 'core/itinerary_create.html', {
        'form': form,
        'destination': destination,
        'user_itineraries': user_itineraries
    })



@login_required
def itinerary_delete(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    if request.method == 'POST':
        itinerary.delete()
        return redirect('itinerary_list')
    return render(request, 'core/itinerary_confirm_delete.html', {'itinerary': itinerary})

@login_required
def add_review(request, slug):
    destination = get_object_or_404(Destination, slug=slug)


    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.destination = destination
            review.save()
            messages.success(request, "Your review has been submitted!")
            return redirect('destination_detail', slug=destination.slug)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm()

    return render(request, 'core/add_review.html', {
        'form': form,
        'destination': destination
    })
