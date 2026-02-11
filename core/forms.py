from django import forms
from .models import Itinerary, Destination, Review
from django.core.exceptions import ValidationError
from django.utils import timezone

class ItineraryForm(forms.ModelForm):
    destinations = forms.ModelMultipleChoiceField(
        queryset=Destination.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select at least one destination for your itinerary."
    )

    class Meta:
        model = Itinerary
        fields = ['name', 'start_date', 'end_date', 'destinations']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Custom validation for dates
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and end:
            if end < start:
                raise ValidationError("End date cannot be before start date.")
            if start < timezone.now().date():
                raise ValidationError("Start date cannot be in the past.")

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            choices=[(i, '⭐' * i) for i in range(1, 6)]
        ),
        help_text="Select your rating (1-5 stars)."
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'border rounded px-2 py-1',
                'placeholder': 'Write your review...'
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5 stars.")
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if not comment or comment.strip() == "":
            raise forms.ValidationError("Comment cannot be empty.")
        return comment