from django.db import models


class Director(models.Model):

    name = models.CharField(max_length=50)
    birthday = models.DateField()

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)


class Film(models.Model):

    title = models.CharField(max_length=120)
    release = models.DateField()
    runtime = models.IntegerField()
    director = models.ForeignKey("Director", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.release})"
