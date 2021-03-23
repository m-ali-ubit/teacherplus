from django.core.management.base import BaseCommand
from django.core.management import call_command

countries_fixture = "teacherplus/utils/fixtures/countries.json"
cities_fixtures = "teacherplus/utils/fixtures/cities.json"


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command("loaddata", countries_fixture, app_label="utils")
        call_command("loaddata", cities_fixtures, app_label="utils")
