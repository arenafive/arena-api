import graphene
from graphene import ClientIDMutation, ObjectType

from api.graphql.types import PlayerNode, ManagerNode
from api.models import Player, Manager


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


class UserMutaion(ObjectType):
    sign_in = SignIn.Field()
