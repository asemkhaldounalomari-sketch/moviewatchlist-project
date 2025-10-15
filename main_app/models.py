from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50),
    rating = models.IntegerField(null=True, blank=True) 
    description = models.TextField(blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    STATUS_CHOICES = [
        ('to-watch', 'To Watch'),
        ('watching', 'Watching'),
        ('watched', 'Watched'),
        ('rated', 'Rated'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to-watch')
    rating = models.IntegerField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    
