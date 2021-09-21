from .models import Client, Video
from django import forms

# class ClientForm(forms.ModelForm):
    
#     class Meta:
#         model = Client
#         first_name = forms.CharField()
#         last_name = forms.CharField()
#         notes = forms.CharField(widget=forms.Textarea, required=False)
#         fields = ["first_name", "last_name", "notes"]


class VideoForm(forms.ModelForm):
    
    class Meta:
        model = Video
        fields = ["client_id", "title", "video"]
