from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            first_name='Rufat',
            last_name='Geydarov',
            surname='Gasrat_ogly',
            email='1@mail.ru',
            is_superuser=True,
            is_staff=True,
        )
        user.set_password('12345')
        user.save()
