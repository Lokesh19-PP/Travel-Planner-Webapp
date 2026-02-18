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
    path('itinerary/<int:pk>/delete/', views.itinerary_delete, name='itinerary_delete'),
    path('destinations/<slug:slug>/review/', views.add_review, name='add_review'),
    path("favorite/add/<int:destination_id>/", views.add_favorite, name="add_favorite"),
    path("favorite/remove/<int:destination_id>/", views.remove_favorite, name="remove_favorite"),
    path("my-favorites/", views.my_favorites, name="my_favorites"),
    path('itinerary/<int:itinerary_id>/add-day/', views.add_itinerary_day, name='add_day'),
    path("itinerary/day/<int:day_id>/add-activity/", views.add_activity, name="add_activity"),
]
