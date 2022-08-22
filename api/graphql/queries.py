import graphene
from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphql_jwt.decorators import login_required

from api.graphql.types import (
    GameNode,
    PlayerNode,
    ArenaNode,
    ManagerNode,
    ArenaFiveSettingsNode,
)
from api.models import ArenaFiveSettings


class GameQuery(ObjectType):
    game = graphene.relay.Node.Field(GameNode, token=graphene.String(required=True))
    games = DjangoFilterConnectionField(GameNode, token=graphene.String(required=True))


class PlayerQuery(ObjectType):
    player = graphene.relay.Node.Field(PlayerNode, token=graphene.String(required=True))
    players = DjangoFilterConnectionField(
        PlayerNode, token=graphene.String(required=True)
    )


class ManagerQuery(ObjectType):
    manager = graphene.relay.Node.Field(
        ManagerNode, token=graphene.String(required=True)
    )
    managers = DjangoFilterConnectionField(
        ManagerNode, token=graphene.String(required=True)
    )


class ArenaQuery(ObjectType):
    arena = graphene.relay.Node.Field(ArenaNode, token=graphene.String(required=True))
    arenas = DjangoFilterConnectionField(
        ArenaNode, token=graphene.String(required=True)
    )


class ArenaFiveSettingsQuery(ObjectType):
    settings = graphene.Field(
        ArenaFiveSettingsNode, token=graphene.String(required=True)
    )

    @login_required
    def resolve_settings(self, info):
        return ArenaFiveSettings.objects.first()
