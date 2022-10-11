from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class Adress(models.Model):
    ville = models.CharField(max_length=100, default="Nouakchott")
    quartier = models.CharField(max_length=200, default="Tevrag Zeina")
    longitude = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.CharField(max_length=500, null=True, blank=True)
    longitudeDelta = models.CharField(max_length=500, null=True, blank=True)
    latitudeDelta = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.ville},{self.quartier} - {self.longitude}°, {self.latitude}°"

    class Meta:
        unique_together = ("ville", "quartier", "description")
        verbose_name_plural = "Adresses"


class TimeStampCreation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Media(TimeStampCreation):
    url = models.CharField(max_length=500)
    arena = models.ForeignKey(
        "api.Arena", on_delete=models.CASCADE, related_name="medias"
    )


class InformationDetails(TimeStampCreation):
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=1000)
    email_adress = models.EmailField(blank=True)
    profile = models.CharField(max_length=5000, null=True, blank=True)
    exponent_push_token = models.CharField(max_length=5000, null=True, blank=True)

    class Meta:
        abstract = True
        unique_together = ["phone_number"]

    def __str__(self):
        return self.email_adress


class Manager(InformationDetails):
    def __str__(self):
        return f"{self.full_name} : {self.email_adress}"


class Player(InformationDetails):
    def __str__(self):
        return f"{self.full_name} : {self.email_adress}"


class Arena(models.Model):
    slug = models.CharField(max_length=255)
    description = models.TextField()
    is_partener = models.BooleanField(default=False)
    note = models.IntegerField()
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        Manager, on_delete=models.CASCADE, related_name="arenas"
    )
    long = models.IntegerField(default=18)
    larg = models.IntegerField(default=12)
    price = models.IntegerField(default=5000)

    def __str__(self):
        return f"Cité {self.slug}"

    class Meta:
        verbose_name = "Arena"
        verbose_name_plural = "Arena"


class Availability(models.Model):
    DAY_CHOICES = [
        ("LUNDI", "LUNDI"),
        ("MARDI", "MARDI"),
        ("MERCREDI", "MERCREDI"),
        ("JEUDI", "JEUDI"),
        ("VENDREDI", "VENDREDI"),
        ("SAMEDI", "SAMEDI"),
        ("DIMANCHE", "DIMANCHE"),
    ]

    day = models.CharField(choices=DAY_CHOICES, max_length=10, blank=False, null=False)
    start_hour = models.IntegerField()
    start_minute = models.IntegerField()
    end_hour = models.IntegerField()
    end_minute = models.IntegerField()
    price = models.IntegerField(default=5000)
    available = models.BooleanField(default=True)

    arena = models.ForeignKey(
        Arena, on_delete=models.CASCADE, related_name="availabilities"
    )

    def __str__(self):
        return f"{self.day}: {self.start_hour}:{self.start_minute} - {self.end_hour}:{self.end_minute}"


class Game(models.Model):
    GAME_CHOICES = [
        ("5", "5 vs 5"),
        ("6", "6 vs 6"),
        ("7", "7 vs 7"),
        ("8", "8 vs 8"),
    ]

    STATUS_CHOICES = [
        ("0", "Waiting for paiment"),
        ("1", "Validated ✅"),
        ("2", "Canceled ❌"),
    ]

    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    type = models.CharField(choices=GAME_CHOICES, max_length=10, default="5")
    arena = models.ForeignKey(
        Arena, null=True, blank=True, on_delete=models.SET_NULL, related_name="games"
    )
    captain = models.ForeignKey(
        Player,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="captains",
    )
    players = models.ManyToManyField(Player, related_name="games")
    score = models.CharField(max_length=20, default="NA")
    reference = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="0")
    amount = models.IntegerField()
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"This Match is organised by {self.captain}"
            if not self.blocked
            else f"This Match is organised by {self.arena.manager.full_name}"
        )


class StarOfTheGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"The man of the match is {self.player}"


class Payment(TimeStampCreation):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    amount = models.IntegerField()
    phone_number = models.CharField(max_length=20)


class BankilyPayment(models.Model):
    payment = GenericRelation(Payment)

    def __str__(self):
        return "By Bankily"


class MasrviPayment(models.Model):
    payment = GenericRelation(Payment)

    def __str__(self):
        return "By Masrvi"


class StripePayment(models.Model):
    payment = GenericRelation(Payment)
    stripe_id = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return "By Stripe"


class PaymentGame(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    to_be_refund = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)

    @property
    def slug(self):
        return f"paiment of {self.player} by {self.payment}"


class ArenaFiveSettings(TimeStampCreation):
    portable = models.CharField(max_length=20, blank=True, null=True)
    fix_number = models.CharField(max_length=20, blank=True, null=True)
    bankily_number = models.CharField(max_length=20, blank=True, null=True)
    bankily_merchant_id = models.CharField(max_length=20, blank=True, null=True)
    maservi_number = models.CharField(max_length=20, blank=True, null=True)
    twitter_link = models.CharField(max_length=500, blank=True, null=True)
    facebook_link = models.CharField(max_length=500, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
