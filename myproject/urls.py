from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('films.urls')),
    # re_path(r'^(?!api(/)?|admin(/)?).*$', TemplateView.as_view(template_name="index.html"), name="entry-point")
]
