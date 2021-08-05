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
    #title = models.CharField(max_length=4, choices=TITLES)
    notes = models.CharField(max_length=1000)
    num_analyses = models.IntegerField(default=0)
    num_videos = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('client', kwargs={'pk': self.pk})


class Video(models.Model):
    title = models.CharField(max_length=500)
    video = models.FileField(upload_to="videos/", default="Nothing")
    print(title)
    print(video)

    def __str__(self):
        return self.title + ": " + str(self.video.path)

    def get_absolute_url(self):
        return reverse('client', kwargs={'pk': self.pk})
    
