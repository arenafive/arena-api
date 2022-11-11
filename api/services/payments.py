import random
import string

import requests
from django.conf import settings

from api.models import BankilyPayment


class BankilyPaymentService:
    def __init__(self):
        self.endpoint = settings.BANKILY_ENDPOINT
        payload = {
            "grant_type": "password",
            "client_id": settings.BANKILY_CLIENT_ID,
            "username": settings.BANKILY_USERNAME,
            "password": settings.BANKILY_PASSWORD,
        }
        response = requests.post(
            url=self.endpoint + "authentification",
            data=payload,
        )
        if response.status_code == 200:
            self.token = response.json()["access_token"]
        else:
            raise f"Bankily api is down {response.content}"

    def pay(self, **kwargs):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(
            url=self.endpoint + "payment", json=kwargs, headers=headers
        )
        return response.json()


def generate_operation_id():
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if BankilyPayment.objects.filter(operation_id=code).count() == 0:
            return code
