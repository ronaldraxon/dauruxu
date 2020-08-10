"""
prediction_dispatcher.views.PredictionView.py
=============================================
Gestiona los puntos finales relacionados con las predicciones
"""

from prediction_dispatcher.views.serializers.PredictionRequestHeaderSerializer import PredictionRequestHeaderSerializer
from prediction_dispatcher.views.serializers.PredictionHeaderSerializer import PredictionHeaderSerializer
from prediction_dispatcher.services.core.PredictionManagementFacadeService import PredictionManagementService

from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


import logging

logger = logging.getLogger(__name__)


class PredictionRequest(generics.GenericAPIView):

    serializer_class = PredictionRequestHeaderSerializer

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo obtiene un conjunto de predicciones dadas
                                 el código y sus respectivas entradas.""",
        responses={
            201: openapi.Response('Solicitud exitosa.', PredictionHeaderSerializer),
            400: openapi.Response('Error en la solicitud.'),
        }))
    def post(request):
        """Gets an existing data asset.

        - **parameters**::
              :param request: Peticion para obtener el serializador

        - **return**::
              :return: Prediction existente con codigo de estado  200 (Solicitud exitosa).
        """
        logger.info("Solicitud para obtener un conjunto de predicciones")
        request_serializer = PredictionRequestHeaderSerializer(data=request.data)
        if request_serializer.is_valid():
            prediction_serializer = PredictionManagementService.create_and_deliver_predictions(request_serializer)
            return Response(prediction_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PredictionReport(generics.GenericAPIView):

    serializer_class = PredictionHeaderSerializer

    param = openapi.Parameter('code', openapi.IN_PATH,
                              description="The code used as identifier.",
                              type=openapi.TYPE_STRING,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo obtiene un conjunto de solicitudes de predicción dado un código identificador.""",
        manual_parameters=[param],
        responses={
            201: openapi.Response('Solicitud exitosa.', PredictionHeaderSerializer),
            400: openapi.Response('Ha especificado un identificador de activos de datos que no está en la base de datos.'),
        }))
    def get(request, code):
        """Obtener los reportes de las predicciones

        - **parameters**::
              :param request: Solicite obtener un conjunto de predicciones.
              :param code: Identificador

        - **return**::
              :return: Obtiene un el reporte de la prediccion con codigo 200 (Solicitud exitosa).
        """
        logger.info("Solicitud para obtener EL conjunto de solicitudes de predicción con código{}".format(code))
        prediction_report_serializer = PredictionHeaderSerializer(PredictionManagementService.
                                                                  get_predictions_report_by_code(code), many=True)
        return Response(prediction_report_serializer.data, status=status.HTTP_200_OK)
