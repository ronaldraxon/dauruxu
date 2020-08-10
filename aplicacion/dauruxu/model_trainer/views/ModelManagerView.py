"""
view.core.ModelManagerView.py
=============================
Module for the ModelManager resources. Responsible for the assignment of model creation tasks, verification of model
metrics and assignment of assignment tasks.
"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from model_trainer.services.mt_core.TrainingManagerService import TrainingManager
from model_trainer.views.serializer.MTSessionSerializer import MTSessionSerializer
from model_trainer.views.serializer.ScheduledTaskSerializer import ScheduledTaskSerializer
from model_trainer.views.serializer.RetrainRequestSerializer import RetrainRequestSerializer
from model_trainer.views.serializer.ForecastModelDBRecordSerializer import ForecastModelDBRecordSerializer
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

logger = logging.getLogger(__name__)


class AsynchronousTrainingRegression(generics.GenericAPIView):
    """Esta clase administra los métodos asociados con las tareas de entrenamiento asincrónicas.
    """
    serializer_class = MTSessionSerializer

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este Metodo programa la tarea de entrenamiento de regresión asociada con un punto y un \
        modelo específico. Las tareas de entrenamiento se ejecutarán de forma asincrónica por el proceso de tareas en segundo plano y su \
        Los resultados se registrarán para consultas posteriores. Es posible experimentar algún retraso en la tarea de entrenamiento \
        creación de registros, ya que hay otros modelos en la cola. Además, el entrenador de modelos programará un modelo \
        encuesta periódicamente después de la finalización de la formación.
        """,
        responses={
            201: openapi.Response('Solicitud exitosa.', MTSessionSerializer),
            400: openapi.Response('Error en la solicitud.'),
        }))
    def post(request):
        logger.info("Post request on model_trainer/async/training_task/regression")
        request_serializer = MTSessionSerializer(data=request.data)
        if request_serializer.is_valid():
            TrainingManager.\
                create_async_regression_training_for_new_point(request_serializer.data['code'],
                                                               request_serializer.data['input_variables'],
                                                               request_serializer.data['response_variable'],
                                                               request_serializer.data['clean_data'])
            return Response(request_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SynchronousTrainingRegression(generics.GenericAPIView):
    """Esta clase gestiona los métodos asociados con las tareas de entrenamiento sincrónicas.
    """
    serializer_class = MTSessionSerializer

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo solicita la tarea de entrenamiento de regresión asociada con un punto y un \
        modelo específico. Las tareas de entrenamiento se ejecutarán sincrónicamente sin la intervención de la tarea en segundo plano \
        y sus resultados se registrarán para consultas posteriores. Es posible experimentar algún retraso en el entrenamiento \
        creación de registros de tareas, ya que hay otros modelos en la cola. Además, el entrenador de modelos programará un modelo \
        encuesta periódicamente después de la finalización de la formación.""",
        responses={
            201: openapi.Response('Solicitud exitosa.', MTSessionSerializer),
            400: openapi.Response('Error en la solicitud.'),
        }))
    def post(request):
        logger.info("Solicitud  al model_trainer")
        request_serializer = MTSessionSerializer(data=request.data)
        if request_serializer.is_valid():
            TrainingManager.\
                create_sync_regression_training_for_new_point(request_serializer.data['code'],
                                                              request_serializer.data['input_variables'],
                                                              request_serializer.data['response_variable'],
                                                              request_serializer.data['clean_data'])
            return Response(request_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReTrainingRegression(generics.GenericAPIView):
    """This class manages the methods associated with synchronous re-training tasks.
    """
    serializer_class = RetrainRequestSerializer

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo solicita el reentrenamiento de regresión para un \
                                 punto existente, proporcionando parámetros de búsqueda de cuadrícula personalizados. La aplicación \
                                 utilizará los datos almacenados.""",
        responses={
            201: openapi.Response('Solicitud exitosa.', RetrainRequestSerializer),
            400: openapi.Response('Error en la solicitud.'),
        }))
    def post(request):
        logger.info("Post request on /sync/re-training_task/regression")
        request_serializer = RetrainRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            TrainingManager.\
                retrain_existing_regression_model_with_code(request_serializer.data['code'],
                                                                  request_serializer.data['param_grid'])
            return Response(request_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainingScheduleInfo(generics.GenericAPIView):
    """Esta clase admisnitra los metodos asociados con el trainer_task
    """
    serializer_class = ScheduledTaskSerializer

    param = openapi.Parameter('code', openapi.IN_PATH,
                              description="The code used as identifier.",
                              type=openapi.TYPE_INTEGER,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""This endpoint gets the training task schedule associated with a point.""",
        manual_parameters=[param],
        responses={
            200: openapi.Response('Solicitud exitosa.', ScheduledTaskSerializer),
            204: openapi.Response('No hay tareas programadas'),
        }))
    def get(request, code):
        """Gets the training task associated with a point and a specific model.

        - **parameters**::
              :param request: Request for get the training task associated with a point and a specific model.
              :param code: Identified code to get the training task.

        - **return**::
              :return: A response with code with status 200 (Solicitud exitosa).
        """
        logger.info("Obtener solicitud {0}".format(code))
        query = TrainingManager.get_scheduled_training_by_code(code)
        if not query:
            response = "No hay tareas programadas para el Codigo {}".format(code)
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        else:
            response = ScheduledTaskSerializer(query, many=True)
            return Response(response.data, status=status.HTTP_200_OK)


class MTPointManagement(generics.GenericAPIView):
    """Esta clase realiza una gestión básica sobre los  modelos
    """

    param = openapi.Parameter('code', openapi.IN_PATH,
                              description="The point identifier.",
                              type=openapi.TYPE_INTEGER,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo obtiene la información completa del modelo""",
        manual_parameters=[param],
        responses={
            201: openapi.Response('Solicitud exitosa.', ForecastModelDBRecordSerializer),
            204: openapi.Response('Ha especificado un codigo que no está en la base de datos.'),
        }))
    def get(request, code):
        """Obtiene la información completa del modelo

        - **parameters**::
              :param request:Solicitud de detalles de un punto.
              :param code: Código  para extracción de datos

        - **return**::
              :return:Respuesta con el detalle del modelo.
        """
        logger.info("Obtener solicitud en point_management{} ".format(code))
        query = TrainingManager.get_model_info_by_code(code)
        if not query:
            response = "No hay registros para el código  especificado {}".format(code)
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        else:
            response = ForecastModelDBRecordSerializer(query, many=True)
            return Response(response.data, status=status.HTTP_200_OK)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Metodo de  eliminacion del punto existente y las tareas a las que está asociado""",
        manual_parameters=[param],
        responses={
            200: openapi.Response('Solicitud exitosa.'),
        }))
    def delete(request, code):
        """Elimina un punto existente y las tareas a las que está asociado.

        - **parameters**::
              :param request: Solicitud de eliminación de un punto
              :param code: Codigo para eliminacion

        - **return**::
              :return:Respuesta con el detalle  y código con estado 200 (Solicitud exitosa).
        """
        logger.info("Solicitud de eliminación de un modelo correspondiente al activo con código {} ".format(code))
        return Response(TrainingManager.delete_model_by_code(code), status=status.HTTP_200_OK)
