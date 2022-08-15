from api.models import Player, Manager


def update_or_create_player(**kwargs):
    return Player.objects.update_or_create(**kwargs)


def update_or_create_manager(**kwargs):
    return Manager.objects.update_or_create(**kwargs)


def get_user(**kwargs):
    user = None
    try:
        user = Player.objects.get(**kwargs)
    except Player.DoesNotExist:
        pass

    if user is None:
        try:
            user = Manager.objects.get(**kwargs)
        except Manager.DoesNotExist:
            raise Exception("error")
    return user
