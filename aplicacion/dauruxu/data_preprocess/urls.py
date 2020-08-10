"""c4ufb.data_registry URL Configuration

"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from data_preprocess.views.DataPreprocessView import DataAssetPreprocessReportGetView
from data_preprocess.views.DataPreprocessView import DataAssetStatisticsGetView
from data_preprocess.views.DataPreprocessView import CleanDataAssetGetView
from data_preprocess.views.DataPreprocessView import DataAssetPreprocessReportPostView

app_name = "data_registry"
urlpatterns = [
                path("report/", DataAssetPreprocessReportPostView.as_view(), name="data_asset_preprocess_report_post"),
                path("report/<int:code>", DataAssetPreprocessReportGetView.as_view(), name="data_asset_preprocess_report_get"),
                path("statistics/<int:code>", DataAssetStatisticsGetView.as_view(), name="data_asset_statistics_get"),
                path("clean_data/<int:code>", CleanDataAssetGetView.as_view(), name="clean_data_asset_get"),
                #path("api/data_management/", DataPreprocessReportList.as_view(), name="data_manager_list"),
                #path("api/data_management/<int:code>", DataPreprocessReportUnit.as_view(), name="data_manager_unit"),
              ]
