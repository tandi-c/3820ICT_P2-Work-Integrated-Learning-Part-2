from .models import Client, Video
from django import forms


# Video upload form
class VideoForm(forms.ModelForm):
    
    class Meta:
        model = Video
        fields = ["client_id", "title", "video"]
