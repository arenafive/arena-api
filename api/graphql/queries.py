import graphene
from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from api.graphql.types import GameNode, PlayerNode, ArenaNode
from api.models import Game
from core.filters import GameFilter, PlayerFilter, ArenaFilter


class GameQuery(ObjectType):
    game = graphene.relay.Node.Field(GameNode)
    games = DjangoFilterConnectionField(GameNode, filterset_class=GameFilter)

    @login_required
    def resolve_games(self, info, **kwargs):
        return Game.objects.all()


class PlayerQuery(ObjectType):
    player = graphene.relay.Node.Field(PlayerNode)
    players = DjangoFilterConnectionField(PlayerNode, filterset_class=PlayerFilter)


class ArenaQuery(ObjectType):
    arena = graphene.relay.Node.Field(ArenaNode)
    arenas = DjangoFilterConnectionField(ArenaNode, filterset_class=ArenaFilter)
