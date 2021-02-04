from django.core.management.base import BaseCommand
from films.models import Director
from ._directors import data


class Command(BaseCommand):
    help = "Populate the Directors table"

    def handle(self, *args, **options):
        directors = []
        for director in data["directors"]:
            try:
                directors.append(Director(**director))
            except Exception as e:
                print(e)


        Director.objects.bulk_create(directors)