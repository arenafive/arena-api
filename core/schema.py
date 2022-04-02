import graphene
import graphql_jwt
from graphene import ObjectType
from graphene_django.debug import DjangoDebug

from api.graphql.mutaions import UserMutaion
from api.graphql.queries import GameQuery, PlayerQuery


class TestNode(ObjectType):
    key = graphene.String()


class Query(GameQuery, PlayerQuery, ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(UserMutaion, ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query, mutation=Mutation)
