import graphene
from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from api.graphql.types import GameNode
from api.models import Game
from core.filters import GameFilter


class GameQuery(ObjectType):
    game = graphene.relay.Node.Field(GameNode)
    games = DjangoFilterConnectionField(GameNode, filterset_class=GameFilter)

    @login_required
    def resolve_games(self, info, **kwargs):
        return Game.objects.all()
