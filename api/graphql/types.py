from graphene import relay
from graphene_django import DjangoObjectType

from api.models import Game, Player, Manager, Media, Arena, Adress


class GameNode(DjangoObjectType):
    class Meta:
        model = Game
        interfaces = (relay.Node,)


class PlayerNode(DjangoObjectType):
    class Meta:
        model = Player
        interfaces = (relay.Node,)


class ManagerNode(DjangoObjectType):
    class Meta:
        model = Manager
        interfaces = (relay.Node,)


class MediaNode(DjangoObjectType):
    class Meta:
        model = Media


class AdressNode(DjangoObjectType):
    class Meta:
        model = Adress


class ArenaNode(DjangoObjectType):
    class Meta:
        model = Arena
        interfaces = (relay.Node,)
