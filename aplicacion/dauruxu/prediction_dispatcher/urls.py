"""c4ufb.data_registry URL Configuration

"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from prediction_dispatcher.views.PredictionView import PredictionRequest
from prediction_dispatcher.views.PredictionView import PredictionReport
app_name = "prediction_dispatcher"

urlpatterns = [
                 path("predict/", PredictionRequest.as_view(), name="prediction_request"),
                 path("report/<str:code>", PredictionReport.as_view(), name="prediction_report")
              ]
