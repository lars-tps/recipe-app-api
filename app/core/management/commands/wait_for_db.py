"""
Django command to wait for DB availability
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for DB availability"""
    def handle(self, *args, **options):
        """Entry point for command"""
        self.stdout.write("Waiting for database...")
        db_up = False

        max_retries = 60
        retries = 0
        while not db_up and retries <= max_retries:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)
                retries += 1

        if not db_up:
            self.stdout.write(self.style.ERROR('Database UNAVAILABLE!'))

        self.stdout.write(self.style.SUCCESS('Database available!'))
