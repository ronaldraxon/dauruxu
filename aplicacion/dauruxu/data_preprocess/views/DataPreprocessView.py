"""
data_preprocess.views.DataPreprocessView.py
===========================================
Módulo para la definición de la vista
de preprocesamiento
"""

from data_preprocess.services.core.DataPreprocessReportService import DataPreprocessReportService
from data_preprocess.views.serializers.DataAssetPreprocessReportGetSerializer import DataAssetPreprocessReportGetSerializer
from data_preprocess.views.serializers.DataAssetPreprocessReportPostSerializer import DataAssetPreprocessReportPostSerializer
from data_preprocess.views.serializers.DataAssetStatisticsGetSerializer import DataAssetStatisticsGetSerializer
from data_preprocess.views.serializers.CleanDataAssetGetSerializer import CleanDataAssetGetSerializer
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response


import logging

logger = logging.getLogger(__name__)


class DataAssetPreprocessReportPostView(generics.GenericAPIView):
    """Esta clase define la vista para solicitar un preprocesamiento de datos.
    """
    serializer_class = DataAssetPreprocessReportPostSerializer

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este método solicita la creación preprocesamiento de un activo de datos existente.""",

        responses={
            201: openapi.Response('Solicitud de creación exitosa.', DataAssetPreprocessReportPostSerializer),
            200: openapi.Response('Solicitud exitosa, pero no se encuentra el código de activo de datos.'),
            400: openapi.Response('Solicitud fallida.'),
        }))
    def post(request):
        """Obtiene el último manifiesto de procesamiento para un activo de datos.

        - **parameters**::
              :param request: Solicitud de extracción de manifiesto de procesamiento de datos.

        - **return**::
              :return: Respuesta de la solicitud.
        """
        logger.info("Solicitud Post para el preprocesamieto de activo de datos ".format(request.data))
        request_serializer = DataAssetPreprocessReportPostSerializer(data=request.data)
        if request_serializer.is_valid():
            #try:
            if DataPreprocessReportService.is_data_asset_in_data_registry(request.data['code']):
                DataPreprocessReportService.create_data_asset_preprocess(request_serializer)
                return Response("bien", status=status.HTTP_201_CREATED)
            else:
            #except DataPreprocessReportService.get_data_asset_from_data_registry(request.data['code']).DoesNotExist:
                response = "No se encuentra el código de activo de datos."
                return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataAssetPreprocessReportGetView(generics.GenericAPIView):
    """Esta clase define la vista para obtener un manifiesto de preprocesamiento de activo de datos.
    """
    serializer_class = DataAssetPreprocessReportGetSerializer
    param = openapi.Parameter('code', openapi.IN_PATH,
                              description="Identificador de activo de datos",
                              type=openapi.TYPE_STRING,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este método obtiene el último manifiesto de preprocesamiento de un activo de datos.""",
        manual_parameters=[param],
        responses={
            200: openapi.Response('Solicitud exitosa.', DataAssetPreprocessReportGetSerializer),
            204: openapi.Response('No se encuentra el código de activo de datos.'),
        }))
    def get(request, code):
        """Obtiene el último manifiesto de procesamiento para un activo de datos.

        - **parameters**::
              :param request: Solicitud de extracción de manifiesto de procesamiento de datos.
              :param code: Identificador del activo de datos que es procesado.

        - **return**::
              :return: Respuesta de la solicitud.
        """
        logger.info("Solicitud get para el manifiesto de preprocesamieto de activo de datos ".format(code, request.data))
        response = DataPreprocessReportService.get_current_data_preprocess_report(code=code)
        if not response:
            return Response("No se encuentra el código de activo de datos.", status=status.HTTP_202_ACCEPTED)
        else:
            return Response(response, status=status.HTTP_204_NO_CONTENT)


class DataAssetStatisticsGetView(generics.GenericAPIView):
    """Esta clase define la vista para obtener las estadísticas
        asociadas al último manifiesto de preprocesamiento de activo de datos.
    """
    serializer_class = DataAssetStatisticsGetSerializer
    param = openapi.Parameter('code', openapi.IN_PATH,
                              description="Identificador de activo de datos",
                              type=openapi.TYPE_STRING,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este método obtiene el último manifiesto de preprocesamiento de un activo de datos.""",
        manual_parameters=[param],
        responses={
            200: openapi.Response('Solicitud exitosa.', DataAssetStatisticsGetSerializer),
            204: openapi.Response('No se encuentra el código de activo de datos.'),
        }))
    def get(request, code):
        """Obtiene las estadísticas relacionadas con el último manifiesto de procesamiento para un activo de datos.

        - **parameters**::
              :param request: Solicitud de extracción de estadisticas de activos de datos.
              :param code: Identificador del activo de datos que es procesado.

        - **return**::
              :return: Respuesta de la solicitud.
        """
        logger.info("Solicitud get para las estadísticas del activo de datos ".format(code, request.data))
        response = DataPreprocessReportService.get_current_data_statistics(code=code)
        if not response:
            return Response("No se encuentra el código de activo de datos.", status=status.HTTP_202_ACCEPTED)
        else:
            return Response(response, status=status.HTTP_204_NO_CONTENT)


class CleanDataAssetGetView(generics.GenericAPIView):
    """Esta clase define la vista para obtener las estadísticas
        asociadas al último manifiesto de preprocesamiento de activo de datos.
    """
    serializer_class = CleanDataAssetGetSerializer
    param = openapi.Parameter('code', openapi.IN_PATH,
                              description="Identificador de activo de datos",
                              type=openapi.TYPE_STRING,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este método obtiene el último manifiesto de preprocesamiento de un activo de datos.""",
        manual_parameters=[param],
        responses={
            200: openapi.Response('Solicitud exitosa.', CleanDataAssetGetSerializer),
            204: openapi.Response('No se encuentra el código de activo de datos.'),
        }))
    def get(request, code):
        """Obtiene las estadísticas relacionadas con el último manifiesto de procesamiento para un activo de datos.

        - **parameters**::
              :param request: Solicitud de extracción de estadisticas de activos de datos.
              :param code: Identificador del activo de datos que es procesado.

        - **return**::
              :return: Respuesta de la solicitud.
        """
        logger.info("Solicitud get para las estadísticas del activo de datos ".format(code, request.data))
        response = DataPreprocessReportService.get_current_clean_data_asset(code=code)
        if not response:
            return Response("No se encuentra el código de activo de datos.", status=status.HTTP_202_ACCEPTED)
        else:
            return Response(response, status=status.HTTP_204_NO_CONTENT)


