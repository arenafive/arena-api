import graphene
from graphene import ClientIDMutation, ObjectType

from api.graphql.types import PlayerNode, ManagerNode
from api.models import Player, Manager
from api.services.twilio import send_sms, verify


class User(graphene.Union):
    class Meta:
        types = (
            PlayerNode,
            ManagerNode,
        )


class SignIn(ClientIDMutation):
    class Input:
        phone_number = graphene.String()
        password = graphene.String()

    user = graphene.Field(User)

    def mutate_and_get_payload(self, info, **input):
        phone_number = input.get("phone_number")
        password = input.get("password")
        user = None
        try:
            user = Player.objects.get(phone_number=phone_number, password=password)
        except Player.DoesNotExist:
            pass

        if user is None:
            try:
                user = Manager.objects.get(phone_number=phone_number, password=password)
            except Manager.DoesNotExist:
                raise Exception("Numero ou mot de passe incorrect !")

        return SignIn(user)


class GenerateCode(ClientIDMutation):
    class Input:
        phone_number = graphene.String()

    verification_sid = graphene.String()
    to = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        verification = send_sms(input.get("phone_number"))
        return GenerateCode(verification_sid=verification.sid, to=verification.to)


class VerifyCode(ClientIDMutation):
    class Input:
        code = graphene.String()
        verification_sid = graphene.String()

    status = graphene.String()
    valid = graphene.Boolean()
    date_created = graphene.DateTime()
    date_updated = graphene.DateTime()

    def mutate_and_get_payload(self, info, **input):
        code = input.get("code")
        verification_sid = input.get("verification_sid")
        verification = verify(code=code, vsid=verification_sid)
        return VerifyCode(
            status=verification.status,
            valid=verification.valid,
            date_created=verification.date_created,
            date_updated=verification.date_updated,
        )


class UserMutaion(ObjectType):
    sign_in = SignIn.Field()
    generate_code = GenerateCode.Field()
    verify_code = VerifyCode.Field()
