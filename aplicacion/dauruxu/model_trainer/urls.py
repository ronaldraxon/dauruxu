"""c4ufb.data_registry URL Configuration

"""

from django.urls import path
from model_trainer.views.ModelManagerView import AsynchronousTrainingRegression,\
                                                 SynchronousTrainingRegression,\
                                                 TrainingScheduleInfo,\
                                                 MTPointManagement,\
                                                 ReTrainingRegression


app_name = "model_trainer"
urlpatterns = [
                path("async/training_task/regression/", AsynchronousTrainingRegression.as_view(), name="async_training_management"),
                path("async/training_task/<str:code>", TrainingScheduleInfo.as_view(), name="training_schedule"),
                path("sync/training_task/regression/", SynchronousTrainingRegression.as_view(), name="sync_training_management"),
                path("sync/re_training_task/regression/", ReTrainingRegression.as_view(), name="re_training_regression"),
                path("point_management/<str:code>", MTPointManagement.as_view(), name="training_schedule"),
              ]
