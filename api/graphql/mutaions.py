import graphene
from graphene import ClientIDMutation, ObjectType

from api.graphql.types import PlayerNode, ManagerNode
from api.services.twilio import send_sms, verify
from api.services.user import update_or_create_player, get_user
from django.contrib.auth import hashers


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
        hashed_password = hashers.make_password(password=password)
        try:

            user = get_user(phone_number=phone_number)
            if not hashers.check_password(password=password, encoded=hashed_password):
                raise Exception("error")
        except Exception:
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


class CreatePlayer(ClientIDMutation):
    class Input:
        full_name = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        password = graphene.String(required=True)

    player = graphene.Field(PlayerNode)

    def mutate_and_get_payload(self, info, **input):
        password = input.get("password")
        phone_number = input.get("phone_number")
        user = None
        try:
            user = get_user(phone_number=phone_number)
        except Exception:
            pass

        if user is None:
            input.update({"password": hashers.make_password(password=password)})

            phone_number = input.get("phone_number")

            user, created = update_or_create_player(
                phone_number=phone_number, defaults={**input}
            )

            return CreatePlayer(player=user)
        raise Exception("Ce numero est deja associé à un compte !")


class VerifyUser(ClientIDMutation):
    class Input:
        phone_number = graphene.String()

    exist = graphene.Boolean()

    def mutate_and_get_payload(self, info, **input):

        phone_number = input.get("phone_number")
        try:
            get_user(phone_number=phone_number)
        except Exception:
            raise Exception("Ce numero n'est associé à aucun compte !")
        return VerifyUser(exist=True)


class ChangePlayerPassword(ClientIDMutation):
    class Input:
        password = graphene.String()
        phone_number = graphene.String()

    created = graphene.Boolean()

    def mutate_and_get_payload(self, info, **input):
        hashed_password = hashers.make_password(password=input.get("password"))
        phone_number = input.get("phone_number")

        try:
            user = get_user(phone_number=phone_number)
            update_or_create_player(pk=user.pk, defaults={"password": hashed_password})
        except Exception:
            raise Exception("error")
        return ChangePlayerPassword(created=True)


class UserMutaion(ObjectType):
    sign_in = SignIn.Field()
    generate_code = GenerateCode.Field()
    verify_code = VerifyCode.Field()
    verify_user = VerifyUser.Field()
    change_player_password = ChangePlayerPassword.Field()
    create_player = CreatePlayer.Field()