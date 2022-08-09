import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from api.models import Game, Player, Manager, Media, Arena, Adress, Availability
from core.filters import GameFilter, PlayerFilter, ArenaFilter


class GameNode(DjangoObjectType):
    class Meta:
        model = Game
        interfaces = (relay.Node,)
        filterset_class = GameFilter


class PlayerNode(DjangoObjectType):
    status = graphene.String()

    class Meta:
        model = Player
        interfaces = (relay.Node,)
        filterset_class = PlayerFilter

    def resolve_status(self, info, **kwargs):
        return self.status


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
        filterset_class = ArenaFilter


class AvailabilityNode(DjangoObjectType):
    class Meta:
        model = Availability
        interfaces = (relay.Node,)
        filterset_class = ArenaFilter
