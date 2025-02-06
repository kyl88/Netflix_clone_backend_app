from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class Movie(models.Model):
    GENRE_CHOICES = [
        ('action','Action'),
        ('comedy','Comedy'),
        ('drama','Drama'),
        ('horror','Horror'),
        ('romance','Romance'),
        ('science_fiction','Science Fiction')
        ('fantasy','Fantasy')
        
    ]
    # Description models
    uu_id = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DataField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    length = models.PositiveBigIntegerField()
    image_card = models.FileField(upload_to='movie_images/')
    image_cover = models.FileField(upload_to='movie_images/')
    video = models.FileField(upload_to='movie_videos/')
    movie_views = models.IntegerField(default=0)

def __str__(self):
    return self.title

class MovieList(models.Model):
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,

    ) 
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)