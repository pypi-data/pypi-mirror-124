from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from django_simple_api_auth.errors import UserCreateErrors

User = get_user_model()


class UserCreate:

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def execute(self) -> User:
        try:
            User.objects.get_by_natural_key(self.username)
            raise ValidationError(UserCreateErrors.USER_ALREADY_EXISTS.value)
        except User.DoesNotExist:
            self.check_password()
            return User.objects.create_user(username=self.username, password=self.password, email=self.username)

    def check_password(self):
        try:
            self.user_validate_password()
        except ValidationError as exc:
            transformed_errors = list(map(lambda error: UserCreateErrors(error.code.upper()).value, exc.error_list))
            raise ValidationError(transformed_errors)

    def user_validate_password(self):
        user = User()
        setattr(user, User.USERNAME_FIELD, self.username)
        validate_password(self.password, user=user)
