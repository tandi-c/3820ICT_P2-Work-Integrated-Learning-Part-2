from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .validators import file_size

# Create your models here.

TITLES = (
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Ms', 'Ms'),
)

class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateTimeField(default=timezone.now)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    notes = models.CharField(max_length=1000, blank=True)
    num_analyses = models.IntegerField(default=0)
    num_videos = models.IntegerField(default=0) 
    videos = []
    analyses = []
    last_updated = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(default="profile_pics/default.jpg")

    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    def get_absolute_url(self):
        return reverse('client', kwargs={'pk': self.pk})


class Video(models.Model):
    client_id = models.ForeignKey(Client, default=None, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=500)
    video = models.FileField(upload_to="videos/", default="Nothing")
    skeleton_video = models.FileField(default="Nothing")
    analysis = models.FilePathField(default="No Analysis")
    analysis_title = models.CharField(max_length=100, default=None, blank=True, null=True)
    date_uploaded = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'

    def __str__(self):
        return self.video.path

    def get_absolute_url(self):
        return reverse('client', kwargs={'pk': self.pk})
    
