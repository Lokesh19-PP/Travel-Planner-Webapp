from django.contrib import admin
from .models import Destination

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'price_range', 'rating')
    search_fields = ('name', 'country')
    list_filter = ('country', 'price_range')

