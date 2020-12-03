import re
from functools import reduce

import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from graphql import GraphQLError

import datetime

from food.models import Menu, Restaurant


class Time(graphene.Enum):
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'


class RestaurantType(DjangoObjectType):
    class Meta:
        model = Restaurant


class MenuType(DjangoObjectType):
    class Meta:
        model = Menu


class Query(graphene.ObjectType):
    menus = graphene.List(MenuType, gte=graphene.Int(), lte=graphene.Int(), date=graphene.String(), time=graphene.Int())
    menu = graphene.Field(MenuType, id=graphene.Int(required=True))
    restaurants = graphene.List(RestaurantType)
    restaurant = graphene.Field(RestaurantType, id=graphene.Int(required=True))

    def resolve_menus(root, info, gte=None, lte=None, date=None, time=None, **kwargs):
        rules = []

        if time and time != 0:
            rules.append(Q(time=time))

        if gte:
            rules.append(Q(price__gte=gte))
        if lte:
            rules.append(Q(price__lte=lte))

        # if date:
        #     pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        #     matched = pattern.findall(date)
        #     y, m, d = map(int, matched[0].split('-'))
        #
        #     print('matched', matched, "::", datdate(y, m, d))


        if date:
            try:
                pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                matched = pattern.findall(date)
                if not matched:
                    return GraphQLError("invalid format")
                else:
                    y, m, d = map(int, matched[0].split('-'))
                    rules.append(Q(date__startswith=datetime.date(y, m, d)))
            except ValueError:
                return GraphQLError("parsing error")

        print(rules)
        if rules:
            filters = reduce(lambda a, i: a & i, rules)
            return Menu.objects.filter(filters)
        else:
            return Menu.objects.all()

    def resolve_menu(root, info, id):
        return Menu.objects.get(id=id)

    def resolve_restaurants(root, info, **kwargs):
        return Restaurant.objects.all()

    def resolve_restaurant(root, info, id):
        return Restaurant.objects.get(id=id)
