from django.core.management.base import BaseCommand
from films.models import Director
from ._directors import data


class Command(BaseCommand):
    help = "Populate the Directors table"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete clear the table',
        )

    def handle(self, *args, **options):
        directors = []
        for director in data["directors"]:
            try:
                if options["clear"]:
                    Director.objects.filter(name=director["name"], birthday=director["birthday"]).delete()
                else:
                    directors.append(Director(**director))
            except Exception as e:
                print(e)


        Director.objects.bulk_create(directors)