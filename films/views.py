from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Director, Film
from .serializers import DirectorSerializer, FilmSerializer

class DirectorAPIView(APIView):

    def get(self, request):
        directors = Director.objects.all()
        item = self.request.query_params.get("item", "")

        if item != "":
            directors = directors.filter(name=item)

        serializer = DirectorSerializer(directors, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = DirectorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DirectorDetailAPIView(APIView):

    def get(self, request, director_id):
        director = get_object_or_404(Director, id=director_id)
        serializer = DirectorSerializer(director)
        return Response(data=serializer.data)