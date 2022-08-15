import random
import string

from django.contrib.auth import hashers
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Game, Manager


def generate_ref_code(model):
    b = True
    code = ""
    while b:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        count = model.objects.filter(reference=code).count()
        if count == 0:
            b = False
    return code


@receiver(
    post_save,
    sender=Game,
)
def game_generate_ref(sender, instance, created, **kwargs):
    if created:
        instance.reference = generate_ref_code(Game)
        instance.save()


@receiver(
    post_save,
    sender=Manager,
)
def hash_password(sender, instance, created, **kwargs):
    hashed_password = hashers.make_password(password=instance.password)
    instance.password = hashed_password
    instance.save()
