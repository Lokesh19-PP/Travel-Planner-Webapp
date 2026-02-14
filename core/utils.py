from .models import Destination, Review
from django.db.models import Avg

def get_filtered_destinations(query_params):
    destinations = Destination.objects.all()
    country = query_params.get("country")
    price = query_params.get("price")
    rating = query_params.get("rating")
    query = query_params.get("search")

    if query:
        destinations = destinations.filter(name__icontains=query)
    if country and country != "All":
        destinations = destinations.filter(country__iexact=country)
    if price and price != "All":
        destinations = destinations.filter(price_range=price)
    if rating and rating != "All":
        try:
            destinations = destinations.filter(rating__gte=float(rating))
        except ValueError:
            pass

    return destinations


def get_average_rating(destination):
    reviews = destination.reviews.all()
    if reviews.exists():
        return round(reviews.aggregate(avg_rating=Avg("rating"))["avg_rating"], 1)
    return 0
