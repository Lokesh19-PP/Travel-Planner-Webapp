from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    price_range = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f"{self.name}, {self.country}"

