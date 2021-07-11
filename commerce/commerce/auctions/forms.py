from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput
from .models import Listing

class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'image', 'description', 'category', 'duration', 'current_bid')
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Give your listing a title...'
            }),
            
            'image': URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a link to an image to use for your listing... (optional)',
            }),

            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Give your listing a description...'
            }),
            'current_bid': NumberInput(attrs={
                'min': 0
            }) 
        }
        labels = {
            'title': '',
            'image': '',
            'description': '',
            'current_bid': 'Starting Bid ($)'
        }