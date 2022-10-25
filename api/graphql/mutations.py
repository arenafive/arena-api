import base64
import graphene

from django.utils import timezone
from graphene import ClientIDMutation, ObjectType

from api.graphql.types import PlayerNode, ManagerNode, GameNode
from api.models import Player, Game, Arena, BankilyPayment, PaymentGame
from api.services.payments import BankilyPaymentService, generate_operation_id
from api.services.twilio import send_sms, verify
from api.services.user import update_or_create_player, get_user, send_notification
from django.contrib.auth import hashers
import logging

logger = logging.getLogger(__name__)


def get_UUID_from_base64(id):
    return base64.b64decode(id).decode().split(":")[1]


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
        token = graphene.String(required=True)

    user = graphene.Field(User)

    def mutate_and_get_payload(self, info, **input):
        input.pop("token")
        phone_number = input.get("phone_number")
        password = input.get("password")
        try:

            user = get_user(phone_number=phone_number)
            if not hashers.check_password(password=password, encoded=user.password):
                raise Exception("error")
        except Exception:
            raise Exception("Numero ou mot de passe incorrect !")

        return SignIn(user)


class GenerateCode(ClientIDMutation):
    class Input:
        phone_number = graphene.String()
        token = graphene.String(required=True)

    verification_sid = graphene.String()
    to = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        verification = send_sms(input.get("phone_number"))
        return GenerateCode(verification_sid=verification.sid, to=verification.to)


class VerifyCode(ClientIDMutation):
    class Input:
        code = graphene.String()
        verification_sid = graphene.String()
        token = graphene.String(required=True)

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
        token = graphene.String(required=True)

    player = graphene.Field(PlayerNode)

    def mutate_and_get_payload(self, info, **input):
        input.pop("token")
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


class UpdatePlayerDetails(ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        full_name = graphene.String(required=False)
        phone_number = graphene.String(required=False)
        email_adress = graphene.String(required=False)
        password = graphene.String(required=False)
        android_exponent_push_token = graphene.String(required=False)
        ios_exponent_push_token = graphene.String(required=False)
        profile = graphene.String(required=False)
        token = graphene.String(required=True)

    player = graphene.Field(PlayerNode)

    def mutate_and_get_payload(self, info, **input):
        input.pop("token")
        id = input.pop("id")
        try:
            player, created = Player.objects.update_or_create(
                pk=get_UUID_from_base64(id), defaults={**input}
            )
            return UpdatePlayerDetails(player=player)

        except Exception as e:
            raise e


class DeleteUserAccount(ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        token = graphene.String(required=True)

    status_code = graphene.String()
    message = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        status_code = "1"
        message = "success"

        input.pop("token")
        id = input.pop("id")
        try:
            player = Player.objects.get(pk=get_UUID_from_base64(id))
            player.delete()
        except Exception as e:
            status_code = 0
            message = e
        return DeleteUserAccount(status_code=status_code, message=message)


class VerifyUser(ClientIDMutation):
    class Input:
        phone_number = graphene.String()
        token = graphene.String(required=True)

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
        token = graphene.String(required=True)

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


class CreateGame(ClientIDMutation):
    class Input:
        amount = graphene.String()
        client_phone = graphene.String()
        passcode = graphene.String()
        language = graphene.String()
        arena_id = graphene.ID()
        captain_id = graphene.ID()
        start_date = graphene.DateTime()
        end_date = graphene.DateTime()
        blocked = graphene.Boolean()
        token = graphene.String(required=True)

    code = graphene.String()
    transactionId = graphene.String()
    errorCode = graphene.Int()
    errorMessage = graphene.String()

    def mutate_and_get_payload(self, info, **input):

        params = {
            "amount": input.get("amount"),
            "clientPhone": input.pop("client_phone"),
            "passcode": input.pop("passcode"),
            "language": input.pop("language"),
            "operationId": generate_operation_id(),
        }
        code = -10
        game = Game.objects.filter(
            start_date=input.get("start_date"), end_date=input.get("end_date")
        )
        if game:
            logger.info("game already exist")
            return CreateGame(
                code=-1,
                **{
                    "transactionId": "",
                    "errorCode": 1,
                    "errorMessage": "Mobile Number is not registered",
                },
            )
        pay_service = BankilyPaymentService()
        res = pay_service.pay(**params)
        logger.info(f"Payment have been processed with result: ({res})")
        if res["errorCode"] == 0:
            p = BankilyPayment.objects.create(
                transaction_id=res["transactionId"], operation_id=params["operationId"]
            )
            payment = p.payment.create(
                amount=params.get("amount"), phone_number=params.get("clientPhone")
            )
            input.pop("token")
            captain_id = input.pop("captain_id", None)
            arena_id = input.pop("arena_id")
            captain = None
            if captain_id:
                captain = Player.objects.get(pk=get_UUID_from_base64(captain_id))
            arena = Arena.objects.get(pk=get_UUID_from_base64(arena_id))
            game = Game.objects.create(
                arena=arena, captain=captain, status="1", **input
            )
            if captain:
                game.players.add(captain)
            PaymentGame.objects.create(payment=payment, game=game, player=captain)
        if game:
            code = game.reference
        return CreateGame(code=code, **res)


class JoinGame(ClientIDMutation):
    class Input:
        code = graphene.String()
        player_id = graphene.ID()
        token = graphene.String(required=True)

    status = graphene.Boolean()
    game = graphene.Field(GameNode)

    def mutate_and_get_payload(self, info, **input):
        player_id = input.pop("player_id")
        code = input.pop("code")
        player = Player.objects.get(pk=get_UUID_from_base64(player_id))
        game = Game.objects.filter(reference=code).first()
        if game:
            if game.captain.pk == player.pk:
                return JoinGame(status=False, game=game)
            if game.start_date < timezone.now():
                return JoinGame(status=False, game=None)
            game.players.add(player)
            send_notification(game=game, message=f"a rejoint votre match du {game.start_date}")
            return JoinGame(status=True, game=game)
        return JoinGame(status=False, game=None)


class CancelGame(ClientIDMutation):
    class Input:
        code = graphene.String()
        token = graphene.String(required=True)

    status = graphene.Boolean()
    game = graphene.Field(GameNode)

    def mutate_and_get_payload(self, info, **input):
        code = input.pop("code")
        game = Game.objects.filter(reference=code).first()
        game.status = "2"
        game.save()
        p = PaymentGame.objects.get(game=game)
        p.to_be_refund(True)
        send_notification(game=game, message=f"Votre match du {game.start_date} vient d'etre annuler, nous procedrons votre remboursement dans un delai de 24h")
        return JoinGame(status=True, game=game)


class UserMutation(ObjectType):
    sign_in = SignIn.Field()
    generate_code = GenerateCode.Field()
    verify_code = VerifyCode.Field()
    verify_user = VerifyUser.Field()
    change_player_password = ChangePlayerPassword.Field()
    create_player = CreatePlayer.Field()
    update_player_details = UpdatePlayerDetails.Field()
    delete_user_account = DeleteUserAccount.Field()


class GameMutation(ObjectType):
    create_game = CreateGame.Field()
    join_game = JoinGame.Field()
    cancel_game = CancelGame.Field()
