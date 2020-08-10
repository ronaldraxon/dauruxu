"""
data_registry.views.DataAssetView.py
====================================
Modulo para la vista del Activo de Datos
"""

from data_registry.models.storage.DataAsset import DataAsset
from data_registry.services.storage.DataAssetService import DataAssetService
from data_registry.views.serializers.DataAssetSerializer import DataAssetSerializer
from data_registry.views.serializers.DataAssetRowSerializer import DataAssetRowSerializer
from data_registry.views.serializers.DataAssetRegistrySerializer import DataAssetRegistrySerializer
from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import logging

logger = logging.getLogger(__name__)


class DataAssetCreation(generics.GenericAPIView):
    """ Clase para administrar el activo de los datos.
    """
    serializer_class = DataAssetRegistrySerializer

    param = openapi.Parameter('code', openapi.IN_PATH,
                              description="The data asset identifier.",
                              type=openapi.TYPE_INTEGER,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo carga un nuevo activo de datos. """,
        responses={
            201: openapi.Response('Solicitud exitosa.', DataAssetSerializer),
            400: openapi.Response('Existen errores en su solicitud'),
        }))
    def post(request):
        """Crea un nuevo activo de datos con datos sin procesar y sus especificaciones.

        - **parameters**::
              :param request: Solicitar con un activo de datos y sus caracteristicas

        - **return**::
              :return:Activo de datos creado con estado 201 (Created).
        """
        logger.info("Solicitud para crear un nuevo activo de datos")
        data_asset_serializer = DataAssetRegistrySerializer(data=request.data)
        if data_asset_serializer.is_valid():
            DataAssetService.create_data_asset(data_asset=data_asset_serializer)
            return Response(data_asset_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data_asset_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataAssetQuery(generics.GenericAPIView):

    param = openapi.Parameter('code', openapi.IN_PATH,
                              description="The data asset identifier.",
                              type=openapi.TYPE_STRING,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Metodo que obtiene un activo de datos por su identificador.""",
        manual_parameters=[param],
        responses={
            201: openapi.Response('Solicitud exitosa.', DataAssetSerializer),
            400: openapi.Response('Ha especificado un identificador de activo de datos que no encuentra en  base de datos.'),
        }))
    def get(request, code):
        """Obtiene un DataAsset existente.

        - **parameters**::
              :param request: Peticion para obtener a data asset .
              :param code: Indentificador del data asset.

        - **return**::
              :return: un  DataAsset existente con estado 200 (Solicitud exitosa).
        """
        logger.info("Solicitud para obtener un activo de datos".format(code, request.data))
        try:
            response = DataAssetSerializer(DataAssetService.retrieve_data_asset(code)).data
            return Response(response, status=status.HTTP_200_OK)
        except DataAsset.DoesNotExist:
            response = "Ha especificado un identificador de activos de datos que no está en la base de datos."
            return Response(response, status=status.HTTP_202_ACCEPTED)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo elimina un activo de datos existente por medio de su identificador""",
        manual_parameters=[param],
        responses={
            200: openapi.Response('Solicitud exitosa.'),
        }))
    def delete(request, code):
        """Eliminar un data asset existente .

        - **parameters**::
              :param request: Peticion para eliminar un data asset.
              :param code: Identificacion de el data asset.

        - **return**::
              :return: Una solicitud exitosa con estado 200 (Solicitud exitosa).
        """
        logger.info("Solicitud para borrar un activo de datos".format(code, request.data))
        return Response(DataAssetService.delete_data_asset(code), status=status.HTTP_200_OK)


class DataAssetUpdate(generics.GenericAPIView):
    """Esta clase actualiza el Activo de datos
    """
    serializer_class = DataAssetRowSerializer

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Carga valores diarios para el activo de datos """,
        responses={
            201: openapi.Response('Solicitud exitosa.', DataAssetRowSerializer),
            400: openapi.Response('Error en la solicitud.'),
        }))
    def put(request):
        """Actualizacion para el activo de datos
        - **parameters**::
              :param request: Peticion para la actualizacion del activo de datos

        - **return**::
              :return: Respuesta con codigo de estado 201 (Created).
        """
        logger.info("Solicitud para actualizacion de  un activo de datos existente".format(request.data))
        data_asset_row_serializer = DataAssetRowSerializer(data=request.data)
        if data_asset_row_serializer.is_valid():
            if DataAssetService.is_an_existing_code(request.data.get('code')):
                return Response(DataAssetService.update_data_asset(request.data.get('code'),
                                                                   data_asset_row_serializer),
                                status=status.HTTP_201_CREATED)
            else:
                response = "Ha especificado un identificador de activo de dato que no existente en la base."
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data_asset_row_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
