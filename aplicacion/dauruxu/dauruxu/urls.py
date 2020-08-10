"""dauruxu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.shortcuts import redirect
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import include


schema_view = get_schema_view(
    openapi.Info(
        title="Dauruxu",
        default_version='v1.0.0',
        description="""This is a project for psycho-social risk assessment assistance. 
        This program was designed by [Ronald Rodríguez](rfernandorodriguez@javeriana.edu.co/) and it is a \
        open software.""",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rfernandorodriguez@javeriana.edu.co"),
        license=openapi.License(name="Open Licence"),
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)


def root_redirect(request):
    return redirect('dauruxu/admin/')


services_urlpatterns = [
    url(r"^dauruxu/", include("user_management.urls")),
    url(r"^dauruxu/data_registry/", include("data_registry.urls", namespace="data_registry")),
    url(r"^dauruxu/data_preprocess/", include("data_preprocess.urls", namespace="data_preprocess")),
    url(r"^dauruxu/model_trainer/", include("model_trainer.urls", namespace="model_trainer")),
    url(r"^dauruxu/data_calendar/", include("data_calendar.urls", namespace="data_calendar")),
    url(r"^dauruxu/prediction_dispatcher/", include("prediction_dispatcher.urls", namespace="prediction_dispatcher")),
    url(r"^dauruxu/apps_administration/", include("apps_administration.urls", namespace="apps_administration"))
]


urlpatterns = [
                  url(r'^dauruxu/admin/', admin.site.urls,
                      name='application-administration'),
                  url(r'^dauruxu/docs/swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
                      name='schema-swagger-ui'),
                  url(r'^$', root_redirect),
              ] + services_urlpatterns



#urlpatterns = [

#    path('', include('user_management.urls')),
#    path('admin/', admin.site.urls),
#]
