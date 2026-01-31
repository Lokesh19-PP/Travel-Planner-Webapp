from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("signup/", views.signup_view, name="signup"),
    path('profile/', views.profile_view, name='profile'),
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('itineraries/', views.itinerary_list, name='itinerary_list'),
    path('itinerary/<int:pk>/', views.itinerary_detail, name='itinerary_detail'),
    path('itinerary/add/', views.itinerary_create, name='itinerary_create'),
]
