from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Adress(models.Model):
    longitude = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.CharField(max_length=500, null=True, blank=True)
    longitudeDelta = models.CharField(max_length=500, null=True, blank=True)
    latitudeDelta = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.longitude}°, {self.latitude}°"


class UserDetail(models.Model):
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email_adress = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Manager(models.Model):
    details = GenericRelation(UserDetail)

    def __str__(self):
        return self.details


class Player(models.Model):
    details = GenericRelation(UserDetail)

    def __str__(self):
        return self.details


class Game(models.Model):
    GAME_CHOICES = [
        ("5", "5 vs 5"),
        ("6", "6 vs 6"),
    ]
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    type = models.CharField(choices=GAME_CHOICES, max_length=10, default="5")
    organised_by = models.ForeignKey(
        Player, null=True, blank=True, on_delete=models.SET_NULL, related_name="captain"
    )
    players = models.ManyToManyField(Player, related_name="game")
    score = models.CharField(max_length=20, default="NA")

    def __str__(self):
        return f"This Match is organised by {self.organised_by}"


class StarOfTheGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"The man of the match is {self.player}"


class Arena(models.Model):
    slug = models.CharField(max_length=255)
    description = models.TextField()
    is_partener = models.BooleanField(default=False)
    note = models.IntegerField()

    adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cité {self.slug}"
