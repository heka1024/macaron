import graphene
from food.schema import Query as MQuery


class Query(MQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
