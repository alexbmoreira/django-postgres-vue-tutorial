from django.test import TestCase

from ..models import Director


class DirectorTests(TestCase):

    def test_NameToTitleCase(self):
        # Arrange
        name = "alFred hitchCoCK"
        director = Director(name=name, birthday="1899-08-13")

        # Act
        director.save()

        # Assert
        self.assertEqual(director.name, "Alfred Hitchcock")