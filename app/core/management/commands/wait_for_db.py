import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('waiting for database')
        conn = None
        while not conn:
            try:
                conn = connections['default']
            except OperationalError:
                self.stdout.write('database unavailable, waiting for 1 sec')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('database avaliable'))
