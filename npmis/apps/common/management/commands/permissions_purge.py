from django.core.management import BaseCommand

from npmis.apps.permissions.models import StoredPermission


class Command(BaseCommand):
    help = 'Remove obsolete permissions from the database'

    def handle(self, *args, **options):
        total = StoredPermission.objects.purge_obsolete()

        self.stdout.write(msg='\n{} obsolete permissions purged.'.format(total))