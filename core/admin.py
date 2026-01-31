from django.contrib import admin
from .models import Destination
from .models import Itinerary

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'price_range', 'rating')
    search_fields = ('name', 'country')
    list_filter = ('country', 'price_range')

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'start_date', 'end_date', 'created_at')
    list_filter = ('start_date', 'end_date', 'user')
    search_fields = ('name', 'user__username')