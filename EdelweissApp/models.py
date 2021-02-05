from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
import os, sys

# Niveaux de Difficulté
class DifficultyLevel(models.IntegerChoices):
    VERYEASY = 0, 'Very Easy'
    EASY = 1, 'Easy'
    MEDIUM = 2, 'Medium'
    HARD = 3, 'Hard'
    VERYHARD = 4, 'Very Hard'

# Types de Randonnée
class HikeType(models.IntegerChoices):
    PEDESTRIAN = 0, 'Pedestrian'
    TRAIL = 1, 'Trail'
    MOUNTAINBIKE = 2, 'Mountain Bike'
    ROADBIKE = 3, 'Mountain Bike'
    SNOWSHOES = 4, 'Snowshoes'
    SKI = 5, 'Ski'
    HORSE = 6, 'Horse'
    CANOE = 7, 'Canoe / Kayak'
    SNORKELING = 8, 'Snorkeling'

# Modèle Randonées
class Hike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    Type = models.IntegerField(default=HikeType.PEDESTRIAN, choices=HikeType.choices)
    difficulty = models.IntegerField(default=DifficultyLevel.MEDIUM, choices=DifficultyLevel.choices)
    distance = models.FloatField(default=0)
    duration = models.IntegerField(default=0,  validators=[
            MaxValueValidator(24*60),
            MinValueValidator(0)
        ])  # en minutes
    loop = models.BooleanField(default=True)
    positiveElevation = models.IntegerField(default=0)
    negativeElevation = models.IntegerField(default=0)
    negativeElevation = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='img' + os.sep + 'hikes' + os.sep, default='', blank=True)

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.thumbnail.url))
        return mark_safe('<img src="/media/img/no-img.png" width="300" height="300" />')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.thumbnail.name))
        super(Hike, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title

# Modèle Point d'Interets

class PointsOfInterest(models.Model):
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE, null=True, verbose_name='Hike')
    title = models.CharField(max_length=200)
    text = models.TextField()
    latitude = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    published = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='img' + os.sep + 'poi' + os.sep, default='', blank=True)

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.thumbnail.url))
        return mark_safe('<img src="/media/img/no-img.png" width="300" height="300" />')

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.thumbnail.name))
        super(PointsOfInterest, self).delete(*args, **kwargs)