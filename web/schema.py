import graphene
import graphql_jwt
import profiles.schema as p
import health_tests.schema as ht


class Query(p.Query, ht.Query, graphene.ObjectType,):
    hello = graphene.String(default_value="Hi!")
    pass


class Mutation(p.Mutation, ht.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
