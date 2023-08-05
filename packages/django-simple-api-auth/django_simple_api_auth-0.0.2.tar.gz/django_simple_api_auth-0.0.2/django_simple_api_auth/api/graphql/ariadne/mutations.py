from abc import ABC, abstractmethod
from typing import Any

from ariadne import MutationType, convert_kwargs_to_snake_case
from django.core.exceptions import ValidationError
from graphql import GraphQLResolveInfo

from django_simple_api_auth.api.graphql.ariadne.mixins import ClientIDMutationMixin
from django_simple_api_auth.business_logic.user_create import UserCreate
from django_simple_api_auth.business_logic.user_login import UserLogin
from django_simple_api_auth.business_logic.user_logout import UserLogout
from django_simple_api_auth.business_logic.user_password_recovery import UserPasswordRecovery
from django_simple_api_auth.business_logic.user_reset_password import UserResetPassword
from django_simple_api_auth.business_logic.user_social_login import UserSocialLogin

mutation = MutationType()


class UserCreateResolver(ClientIDMutationMixin):

    def mutate(self, obj: Any, info: GraphQLResolveInfo, **data):
        try:
            UserCreate(**data['input']).execute()
            return {"ok": True}
        except ValidationError as exc:
            return {"ok": False, "errors": exc.messages}


mutation.set_field("userCreate", UserCreateResolver())


class UserLoginResolver(ClientIDMutationMixin):
    def mutate(self, obj: Any, info: GraphQLResolveInfo, **data):
        try:
            UserLogin(request=info.context['request'], **data['input']).execute()
            return {'ok': True}
        except ValidationError as exc:
            return {'ok': False, 'errors': exc.messages}


mutation.set_field("userLogin", UserLoginResolver())


class UserLogoutResolver(ClientIDMutationMixin):
    def mutate(self, obj: Any, info: GraphQLResolveInfo, **data):
        try:
            UserLogout(request=info.context['request']).execute()
            return {'ok': True}
        except ValidationError as exc:
            return {'ok': False, 'errors': exc.messages}


mutation.set_field("userLogout", UserLogoutResolver())


class UserPasswordRecoveryResolver(ClientIDMutationMixin):
    def mutate(self, obj: Any, info: GraphQLResolveInfo, **data):
        input = data['input']
        UserPasswordRecovery(info.context['request'], input.get('email')).execute()
        return {'ok': True}


mutation.set_field("userPasswordRecovery", UserPasswordRecoveryResolver())


class UserResetPasswordResolver(ClientIDMutationMixin):
    def mutate(self, obj: Any, info: GraphQLResolveInfo, **data):
        try:
            UserResetPassword(**data['input']).execute()
            return {'ok': True}
        except ValidationError as exc:
            return {'ok': False, 'errors': exc.messages}


mutation.set_field("userResetPassword", UserResetPasswordResolver())


class UserSocialLoginResolver(ClientIDMutationMixin):

    @convert_kwargs_to_snake_case
    def mutate(self, obj: Any, info: GraphQLResolveInfo, **data):
        try:
            UserSocialLogin(request=info.context['request'], **data['input']).execute()
            return {'ok': True}
        except ValidationError as exc:
            return {'ok': False, 'errors': exc.messages}


mutation.set_field("userSocialLogin", UserSocialLoginResolver())
