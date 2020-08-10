"""apps_administration.urls.py
==============================
"""

from django.urls import path
from apps_administration.views.PropertyView import PropertyList, PropertyUnit, DefaultProperties


app_name = "apps_administration"
urlpatterns = [
                path("property/default/", DefaultProperties.as_view(), name="property_list"),
                path("property/", PropertyList.as_view(), name="property_list"),
                path("property/<str:key>", PropertyUnit.as_view(), name="property_unit"),
              ]
