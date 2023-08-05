from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = 'Implement here your custom logic for loading data, this command is going to be executed when the data' \
           ' base is created at first time, after migrating. You can customize the command using arguments and env vars.' \
           'This example is created prioritizing the argument option. '

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--create_super_user',
            action='store_true',
            dest='create_super_user',
            help="Create a superuser",
        )

    def handle(self, *args, **options):
        if options['create_super_user']:
            self.create_super_user()
        elif settings.CREATE_SUPER_USER:
            self.create_super_user()

    @staticmethod
    def create_super_user():
        if User.objects.filter(email=settings.DEFAULT_SUPER_USER_EMAIL).exists():
            return
        try:
            user = User.objects.create_superuser(
                username=settings.DEFAULT_SUPER_USER_EMAIL,
                email=settings.DEFAULT_SUPER_USER_EMAIL,
                password=settings.DEFAULT_SUPER_USER_PASSWORD,
            )
            print('Super user created')
        except Exception as exc:
            raise CommandError(exc)
