from graphene import relay
from graphene_django import DjangoObjectType

from api.models import Game


class GameNode(DjangoObjectType):
    class Meta:
        model = Game

        interfaces = (relay.Node,)
