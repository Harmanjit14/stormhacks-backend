import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import Profile
from graphql import GraphQLError
from django.db.models import Q


# Graphene Objects
class Profile_Object(DjangoObjectType):
    class Meta:
        model = Profile


class User_Object(DjangoObjectType):
    class Meta:
        model = get_user_model()


# Query
class Query(graphene.ObjectType):
    get_me = graphene.Field(Profile_Object)
    get_highscore = graphene.List(Profile_Object)

    # def resolve_locationUser(self, info, location=None, **kwargs):
    #     u = info.context.user
    #     if u.is_anonymous:
    #         raise GraphQLError("Not Logged In!")
    #     if location:
    #         filter = (
    #             Q(city__icontains=location) |
    #             Q(state__icontains=location)
    #         )
    #     return UserProfile.objects.filter(filter)

    def resolve_get_highscore(self, info, **kwargs):
        u = info.context.user
        if u.is_anonymous:
            raise GraphQLError("Not Logged In!")

        return Profile.objects.all().order_by("-high_score")

    def resolve_get_me(self, info):
        u = info.context.user
        if u.is_anonymous:
            raise GraphQLError("Not Logged In!")
        return Profile.objects.get(user=u)


class CreateUser(graphene.Mutation):
    user = graphene.Field(User_Object)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        age = graphene.Int(required=True)
        gender = graphene.String(required=True)
        city = graphene.String()
        state = graphene.String()
        country = graphene.String()

    def mutate(self, info, username, password, email, name, age, gender, **kwargs):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        city = kwargs.get('city')
        state = kwargs.get('state')
        country = kwargs.get('country')

        profile = Profile.objects.create(
            user=user, name=name, age=age, gender=gender, city=city, state=state, country=country)
        profile.save()

        return CreateUser(user=user)


class UpdateScore(graphene.Mutation):
    update = graphene.Field(Profile_Object)

    class Arguments:
        score = graphene.Int(required=True)

    def mutate(self, info, score, **kwargs):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")

        profile = Profile.objects.get(user=user)
        profile.last_score = score
        profile.high_score = max(score, profile.high_score)
        profile.save()

        return UpdateScore(update=profile)


class UpdateLife(graphene.Mutation):
    update = graphene.Field(Profile_Object)

    class Arguments:
        life = graphene.Int(required=True)

    def mutate(self, info, life, **kwargs):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")

        profile = Profile.objects.get(user=user)
        profile.game_lives = life
        profile.save()

        return UpdateScore(update=profile)


class DeleteUser(graphene.Mutation):
    user = graphene.String()

    def mutate(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")

        user.delete()
        str = "Done!"

        return DeleteUser(user=str)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_score = UpdateScore.Field()
    update_life = UpdateLife.Field()
    delete_user = DeleteUser.Field()
