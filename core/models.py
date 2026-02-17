from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    price_range = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    slug = models.SlugField(unique=True, blank=True, null=True)  # new field for URL
    tag = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.country}"

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    destinations = models.ManyToManyField('Destination', related_name='itineraries')
    name = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user.username}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(
        'Destination',
        related_name='reviews',
        on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.destination.name} ({self.rating})"
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "destination")

    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"
    
class ItineraryDay(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name="days")
    date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.itinerary.name} — Day {self.id} ({self.date})"


class Activity(models.Model):
    day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name="activities")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.day.itinerary.name} - {self.title}"
