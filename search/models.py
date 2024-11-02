from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

class Actor(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Show(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    actors = models.ManyToManyField(Actor, related_name='shows')  # Ensure no `through` argument is here

    def __str__(self):
        return self.title

class Season(models.Model):
    number = models.PositiveIntegerField()
    show = models.ForeignKey(Show, related_name='seasons', on_delete=models.CASCADE)

    def __str__(self):
        return f"Season {self.number} of {self.show.title}"

class Episode(models.Model):
    title = models.CharField(max_length=100)
    show = models.ForeignKey(Show, related_name='episodes', on_delete=models.CASCADE)
    release_date = models.DateField()
    season = models.ForeignKey(Season, related_name='episodes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} (Season {self.season.number})"

class Subtitle(models.Model):
    episode = models.ForeignKey(Episode, related_name='subtitles', on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    text = models.TextField()  # Full subtitle text for reference
    search_vector = SearchVectorField(null=True, blank=True)  # Full-text search index

    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]  # Full-text search indexing

    def __str__(self):
        return f"{self.language} subtitle for {self.episode.title}"
