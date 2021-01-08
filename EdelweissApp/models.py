from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe

# Niveaux de Difficulté
class DifficultyLevel(models.IntegerChoices):
    VERYEASY = 0, 'Very Easy'
    EASY = 1, 'Easy'
    MEDIUM = 2, 'Medium'
    HARD = 3, 'Hard'
    VERYHARD = 4, 'Very Hard'

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
    cumulativeElevation = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='media/', default='images/no-img.png')

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.thumbnail.url))
        return ""

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title