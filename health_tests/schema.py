from msilib.schema import Class
import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import UserMood
from graphql import GraphQLError
from django.db.models import Q


class Mood_Object(DjangoObjectType):
    class Meta:
        model = UserMood


class Query(graphene.ObjectType):
    get_my_mood = graphene.List(Mood_Object)

    def resolve_get_my_mood(self, info):
        u = info.context.user
        if u.is_anonymous:
            raise GraphQLError("Not Logged In!")

        return UserMood.objects.filter(user=u).order_by("-date")


class UpdateMood(graphene.Mutation):
    update = graphene.Field(Mood_Object)

    class Arguments:
        mood = graphene.Int(required=True)

    def mutate(self, info, mood, **kwargs):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")

        mood_object = UserMood.objects.create(user=user, mood_score=mood)
        mood_object.save()

        return UpdateMood(update=mood_object)


class Mutation(graphene.ObjectType):
    update_mood = UpdateMood.Field()
