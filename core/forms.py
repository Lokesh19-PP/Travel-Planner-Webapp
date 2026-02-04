from django import forms
from .models import Itinerary, Destination
from .models import Review

class ItineraryForm(forms.ModelForm):
    destinations = forms.ModelMultipleChoiceField(
        queryset=Destination.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Itinerary
        fields = ['name', 'start_date', 'end_date', 'destinations']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):
    # Replace numeric input with star-based radio buttons
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            choices=[(i, '⭐' * i) for i in range(1, 6)]
        )
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

    # Keep the validation
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