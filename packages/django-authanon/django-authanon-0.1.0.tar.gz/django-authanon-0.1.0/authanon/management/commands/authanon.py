from django.core.management.base import BaseCommand

from authanon.backends import display_permissions


class Command(BaseCommand):
    help = "Shows the permissions for anonymous and logged in users. Groups will be created if they do not yet exist."

    def handle(self, *args, **options):
        display_permissions()
