from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create Default groups'

    def handle(self, *args, **kwargs):
        group_list = ['Super Admin', 'Doctor', 'Patient', 'Examiner']
        for group in group_list:
            new_group, created = Group.objects.get_or_create(name=group)
            if created:
                self.stdout.write("Group Successfully Created")

