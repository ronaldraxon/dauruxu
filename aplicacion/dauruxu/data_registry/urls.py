"""
data_registry.urls.py
=====================
Modulo para el manejo de las urls de  la aplicacion
"""

from django.urls import path
from data_registry.views.DataAssetView import DataAssetCreation, DataAssetQuery,DataAssetUpdate

app_name = "data_registry"
urlpatterns = [
                path("data-asset/create/", DataAssetCreation.as_view(), name="data_asset_creation"),
                path("data-asset/<str:code>", DataAssetQuery.as_view(), name="data_asset_query"),
                path("data-asset/update/", DataAssetUpdate.as_view(), name="data_asset_update"),
              ]
