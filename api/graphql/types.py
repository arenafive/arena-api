from graphene import relay
from graphene_django import DjangoObjectType

from api.models import (
    Game,
    Player,
    Manager,
    Media,
    Arena,
    Adress,
    Availability,
    ArenaFiveSettings,
)
from core.filters import GameFilter, PlayerFilter, ArenaFilter, ManagerFilter


class GameNode(DjangoObjectType):
    class Meta:
        model = Game
        interfaces = (relay.Node,)
        filterset_class = GameFilter
        convert_choices_to_enum = False


class PlayerNode(DjangoObjectType):
    class Meta:
        model = Player
        interfaces = (relay.Node,)
        filterset_class = PlayerFilter


class ManagerNode(DjangoObjectType):
    class Meta:
        model = Manager
        interfaces = (relay.Node,)
        filterset_class = ManagerFilter


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


class ArenaFiveSettingsNode(DjangoObjectType):
    class Meta:
        model = ArenaFiveSettings
