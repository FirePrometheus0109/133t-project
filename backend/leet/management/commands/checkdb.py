from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = 'Exit code 0 if connected to default DB, 1 if fail to connect'

    def handle(self, *args, **options):
        db_conn = connections['default']
        db_conn.cursor()
        print('Database connection is ok')
