import graphene
import graphql_jwt
from graphene import ObjectType
from graphene_django.debug import DjangoDebug

from api.graphql.mutations import UserMutation, GameMutation
from api.graphql.queries import GameQuery, PlayerQuery, ArenaQuery


class TestNode(ObjectType):
    key = graphene.String()


class Query(ArenaQuery, GameQuery, PlayerQuery, ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(GameMutation, UserMutation, ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query, mutation=Mutation)
