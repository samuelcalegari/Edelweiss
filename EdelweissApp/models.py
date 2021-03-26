from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django_resized import ResizedImageField
from django.utils.deconstruct import deconstructible
import os
import re
import sys

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        print(filename, file=sys.stderr)
        print(instance, file=sys.stderr)
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(re.sub(r"[^a-z0-9]", "-", instance.title.lower()), ext)
        # return the whole path to the file

        return os.path.join(self.path, filename)

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

# Modèle Randonnées
class Hike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
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
    latitude = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    published = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='img/hikes/', default='', blank=True)

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.thumbnail.url))
        return mark_safe('<img src="/media/img/no-img.png" width="300" height="300" />')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def delete(self, *args, **kwargs):
        if self.thumbnail.name != '':
            self.thumbnail.storage.delete(self.thumbnail.name)
        super(Hike, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title

# Modèle Point d'Interets
class PointsOfInterest(models.Model):
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE, null=True, verbose_name='Hike')
    title = models.CharField(max_length=200, null=True)
    text = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    published = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='img/poi/', default='', blank=True)

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.thumbnail.url))
        return mark_safe('<img src="/media/img/no-img.png" width="300" height="300" />')

    def delete(self, *args, **kwargs):
        if self.thumbnail.name != '':
            self.thumbnail.storage.delete(self.thumbnail.name)
        super(PointsOfInterest, self).delete(*args, **kwargs)

# Modèle Badges
class Badge(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    thumbnail = ResizedImageField(size=[300, 300], upload_to=PathAndRename('img/badges/'), default='', blank=True, force_format='PNG')

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.thumbnail.url))
        return mark_safe('<img src="/media/img/no-img.png" width="300" height="300" />')

    def delete(self, *args, **kwargs):
        self.thumbnail.storage.delete(self.thumbnail.name)
        super(Badge, self).delete(*args, **kwargs)

# Extension du modèle User
class Hiker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)

# Modèle Randonnée Favorite
class FavoriteHike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='User')
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE, null=True, verbose_name='Hike')

# Modèle Randonnée Effectuée
class PerformedHike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='User')
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE, null=True, verbose_name='Hike')