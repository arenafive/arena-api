import json
import requests
import logging

from api.models import Player, Manager
from django.forms import model_to_dict

logger = logging.getLogger(__name__)


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


def send_notification(game, message):
    headers = {
        "Content-Type": "application/json",
    }
    json_data = model_to_dict(game)
    json_data.update({"startDate": game.start_date, "endDate": game.end_date})
    data1 = {
        "to": game.captain.android_exponent_push_token,
        "title": game.captain.full_name,
        "body": message,
        "data": {
            "key": "Game",
            "obj": {"game": json.dumps(json_data, default=str)},
        },
    }
    data2 = {
        "to": game.captain.ios_exponent_push_token,
        "title": game.captain.full_name,
        "body": message,
        "data": {
            "key": "Game",
            "obj": {"game": json.dumps(json_data, default=str)},
        },
    }
    logger.info(f"Sending push notification for android with payload({data1})")
    res = requests.post(
        "https://exp.host/--/api/v2/push/send",
        headers=headers,
        data=json.dumps(data1),
    )
    logger.info(f"Sending push notification for ios with payload({data2})")
    requests.post(
        "https://exp.host/--/api/v2/push/send",
        headers=headers,
        data=json.dumps(data2),
    )
    logger.info(f"response  for android({res})")
    logger.info(f"response for ios ({res})")
