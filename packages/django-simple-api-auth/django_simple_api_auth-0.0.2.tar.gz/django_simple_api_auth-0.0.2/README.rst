Django Simple Api Auth
########################


Django Simple Api Auth is a Django app to help developers with the Session auth of a rest or graphql api in Django.

- Django Rest Framework
- Graphene
- Ariadne

Features
*********

- Create user
- Login
- Logout
- Social login
- Get user data (Me)
- Recover user password
- Overwrite emails
- Overwrite Me fields (Not implemented for ariadne)
- Reset password vía API

Overview
*********

You should read about the CSRF protection in `django <https://docs.djangoproject.com/en/3.2/ref/csrf/>`_

* You have to send X-CSRFToken token in headers
* Rest framework disable csrf in views using csrf_exempt, and adding the validation to the SessionAuthentication
* Graphene don't do anything with the csrf validation, so you have to exempt them when it makes sense. You can use the view of this `example <https://github.com/mrmilu/django-simple-api-auth-example/blob/master/graphqls/views.py>`_ or create your own. Don't disable it for all the endpoints.

Quick start
************



Add django_simple_api_auth and dependencies to your INSTALLED_APPS setting like this::


    INSTALLED_APPS = [
        ...
        'rest_framework',
        'graphene_django',
        'social_django',
        'ariadne.contrib.django',
        'django_simple_api_auth',
    ]


Rest framework
***************

You can add the main ViewSet that has all the permissions and features implemented to your router::

    router.register(r'users', UserApiViewSet, 'users')

Or you can use mixins to create your own viewset::

    class UserCompleteViewSet(UserCreateMixin, UserLoginMixin, UserMeMixin, UserPasswordRecoveryMixin, UserLogoutMixin, UserSocialLoginMixin):
        pass

Graphene
*********

You can add the user queries and mutations to your schema::



    from django_simple_api_auth.api.graphql.mutations import UsersMutation
    from django_simple_api_auth.api.graphql.queries import UserQuery


    class Query(UserQuery, graphene.ObjectType):
        pass


    class Mutation(UsersMutation, graphene.ObjectType):
        pass


    schema = graphene.Schema(
        query=Query,
        mutation=Mutation
    )


or you can create your own query and mutation::

    class UsersMutation(graphene.ObjectType):
        user_create = UserCreateMutation.Field()
        user_login = UserLoginMutation.Field()
        user_social_login = UserSocialLoginMutation.Field()
        user_logout = UserLogoutMutation.Field()
        user_password_recovery = UserPasswordRecoveryMutation.Field()
        user_reset_password = UserResetPasswordMutation.Field()

    class UserQuery(ObjectType):
        get_me = Field(AuthUserType)

        @login_required
        def resolve_get_me(self, info, **kwargs):
            return info.context.user



Ariadne
*********

You have to add the user queries and mutations to your schema manually::

    type Mutation {
        userCreate(input: UserCreateMutationInput!): UserCreateMutationPayload
        userLogin(input: UserLoginMutationInput!): UserLoginMutationPayload
        userLogout(input: UserLogoutMutationInput!): UserLogoutMutationPayload
        userPasswordRecovery(input: UserPasswordRecoveryMutationInput!): UserPasswordRecoveryMutationPayload
        userResetPassword(input: UserResetPasswordMutationInput!): UserResetPasswordMutationPayload
        userSocialLogin(input: UserSocialLoginMutationInput!): UserSocialLoginMutationPayload
    }

    type Query {
        getMe: AuthUserType
    }


and then you have to add types and ObjectTypes to your executable schema, for example::

    import os

    from ariadne import make_executable_schema, gql, load_schema_from_path
    import django_simple_api_auth.api.graphql.ariadne
    from django_simple_api_auth.api.graphql.ariadne.mutations import mutation as auth_mutations
    from django_simple_api_auth.api.graphql.ariadne.queries import query as auth_query
    from example.graphqls.ariadne.queries import query

    auth_types_graphql_dirname = os.path.dirname(django_simple_api_auth.api.graphql.ariadne.__file__)
    auth_mutations_type_defs = gql(load_schema_from_path(f"{auth_types_graphql_dirname}/mutations.graphql"))
    auth_queries_type_defs = gql(load_schema_from_path(f"{auth_types_graphql_dirname}/queries.graphql"))
    type_defs = gql(load_schema_from_path('./graphqls/ariadne/scheme.graphql'))

    type_defs_list = [
        auth_mutations_type_defs,
        auth_queries_type_defs,
        type_defs,
    ]
    schema = make_executable_schema([*type_defs_list], [auth_mutations, auth_query, query])


Create user
*************

User creation is based on BaseUserManager and it manages if you override the USERNAME_FIELD of the user model to use the email field for authentication and login.

Social login
*************

We have the endpoints available to use the `social-app-django <https://github.com/python-social-auth/social-app-django>`_ so read their doc to use it.


Recover user password
**********************

By default, email sent to recover user password has a link to 's/accounts/reset'. The easiest way of handle this is to use the django admin views but you can overwrite the REMEMBER_PASSWORD_URL to send to another location.
If you want to use the default  link you have to add admin views to your project:

add to your settings::

    REMEMBER_PASSWORD_URL = 'front-endpoint'


add to your views::

    path('accounts/', include('django.contrib.auth.urls')),

If you handle de remember password in your frontend, you can use the reset-password endpoint.

Overwrite emails
*****************

You can overwrite emails templates adding new templates to your project::


    - project_name/
        - project_name/
        - templates/
            emails/
                password_recovery/
                    email.html
                    subject.txt
          manage.py


Overwrite Me fields
********************

You can overwrite default fields that the rest and graphql endpoint returns for an authenticated user updating the ME_FIELDS settings::

    ME_FIELDS = ("id", "email",)


this feature can't be implemented for ariadne because of the schema first approach.
