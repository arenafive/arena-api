import random
import string

from twilio.rest import Client
from twilio.rest.verify.v2.service.verification_check import VerificationCheckInstance

from core.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SERVICE
from twilio.rest.verify.v2.service.verification import VerificationInstance


def create_ref_code():
    return "".join(random.choices(string.digits + string.digits, k=6))


def send_sms(phone_number: str) -> VerificationInstance:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    verification = client.verify.services(TWILIO_SERVICE).verifications.create(
        to=phone_number,
        channel=VerificationInstance.Channel.SMS,
    )
    return verification


def verify(vsid: str, code: str) -> VerificationCheckInstance:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    verification = client.verify.services(TWILIO_SERVICE).verification_checks.create(
        verification_sid=vsid, code=code
    )

    return verification
