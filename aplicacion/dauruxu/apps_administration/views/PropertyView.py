"""
apps_administration.views.PropertyView.py
=========================================
Modulo para gestionar los recursos de la propiedades.
Gestiona las propiedades de la aplicación.
"""

from rest_framework.response import Response
from rest_framework import status
from apps_administration.views.serializers.PropertyListSerializer import PropertyListSerializer
from apps_administration.services.PropertyService import PropertyService
from rest_framework import generics
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

logger = logging.getLogger(__name__)


class DefaultProperties(generics.GenericAPIView):
    serializer_class = PropertyListSerializer

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Crea una lista predeterminada de propiedades.""",
        responses={
            200: openapi.Response('Solicitud exitosa.', PropertyListSerializer)
        }))
    def get( request ):
        """Creacion de las propiedades por defecto.

        - **parameters**::
              :param request: Solicitud para crear un conjunto predeterminado de propiedades.
        - **return**::
              :return: La propiedad con codigo de estado 200 (Solicitud exitosa).
        """
        logger.info("Creacion de propiedades por defecto")
        return Response(PropertyListSerializer(PropertyService.create_default_properties(), many=True).data,
                        status=status.HTTP_200_OK)


class PropertyList(generics.GenericAPIView):
    """Gestiona los métodos generales sobre las propiedades de la aplicación
    """
    serializer_class = PropertyListSerializer

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo obtiene una  propiedad registrada""",
        responses={
            200: openapi.Response('Solicitud exitosa.', PropertyListSerializer)
        }))
    def get( request ):
        """Obtiene una propiedad

        - **parameters**::
              :param request:Solicitud para obtener una propiedad.

        - **return**::
              :return: Propiedad con el estado 200 (Solicitud exitosa).
        """
        return Response(PropertyListSerializer(PropertyService.retrieve_all_properties(), many=True),
                        status=status.HTTP_200_OK)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo inserta una nueva propiedad en el sistema.

        Properties:

        FTP_HOSTNAME = The FTP server ip address
        FTP_PASSWORD = The FTP server password
        FTP_PORT = The FTP server port
        FTP_USERNAME = The FTP server user name
        LOCAL_PATH = The local root path in the FTP server where the models and scalers will be stored
        MODEL_FILE_PREFIX = The model file prefix
        PATH_TO_MODEL_FILES = Local folder path to the model files
        PATH_TO_SCALER_FILES = Local folder path to the scalers files
        REMOTE_PATH_SCALER = Folder path to the scaler files in the FTP server
        REMOTE_PATH_MODEL = Folder path to the model files in the FTP server
        SCALER_FILE_PREFIX = The scaler file prefix
        LOW_BOUNDARY_DAY = Minimum days of mt_core
        HIGH_BOUNDARY_DAY = Maximum days of mt_core
        CHECK_DATA_BEHAVIOR = Thresshold for data verifications (Default 30 days).""",
        responses={
            200: openapi.Response('Solicitud exitosa.', PropertyListSerializer),
        }))
    def post( request ):
        """Crea una nueva propiedad.

        - **parameters**::
              :param request: Solicitud para crear una nueva propiedad.

        - **parameters**::
              :return: Una respuesta con la propiedad y el código con el estado 201 (Creado).
        """
        # TODO:: CORREGUIR AQUI
        logger.info("Post request para ")
        property_serializer = PropertyListSerializer(data=request.data)
        if property_serializer.is_valid():
            PropertyService.create_property(property_serializer=property_serializer)
            return Response(property_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(property_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyUnit(generics.GenericAPIView):
    serializer_class = PropertyListSerializer

    param = openapi.Parameter('key', openapi.IN_PATH,
                              description="The point identifier.",
                              type=openapi.TYPE_STRING,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo obtiene una propiedad por su llave""",
        manual_parameters=[param],
        responses={
            200: openapi.Response('Solicitud exitosa.', PropertyListSerializer),
        }))
    def get( request, key ):
        logger.info("Get request on /api/property/[Request details: {}]".format(key))
        return Response(PropertyService.retrieve_property(key), status=status.HTTP_200_OK)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Este metodo borra una propiedad especifica por su llave.""",
        manual_parameters=[param],
        responses={
            200: openapi.Response('Solicitud exitosa.', PropertyListSerializer),
        }))
    def delete( request, key ):
        logger.info("Soliciut de eliminacion  [Request details: {}]".format(key, request.data))
        return Response(PropertyService.delete_point(key), status=status.HTTP_200_OK)




