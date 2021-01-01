from rest_framework import serializers
from .models import Director, Film

class DirectorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Director
        fields = ['name', 'birthday']

class FilmSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Film
        fields = ['title', 'release', 'runtime', 'director']