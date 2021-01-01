from django.urls import path

from .views import DirectorAPIView, DirectorDetailAPIView

director_api = DirectorAPIView.as_view()
director_detail_api = DirectorDetailAPIView.as_view()

urlpatterns = [
    path("directors", director_api, name="directors"),
    path("directors/<int:director_id>", director_detail_api, name="director-detail"),
]
