"""
data_calendar.views.CalendarView.py
===================================
Modulo para los recursos del calendario
"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.conf import settings
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from data_calendar.models.Calendar import Calendar
from data_calendar.services.CalendarService import CalendarService
from data_calendar.services.datemanagement import DateUtil
from data_calendar.views.serializer.CalendarSerializer import CalendarSerializer

logger = logging.getLogger(__name__)


class CalendarGeneration(generics.GenericAPIView):
    """Clase para los recursos del calendario
    """
    serializer_class = CalendarSerializer
    param = openapi.Parameter('year', openapi.IN_PATH,
                              description="The year of the calendar you need to build",
                              type=openapi.TYPE_INTEGER,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Genera un calendario con un año específico. El calendario generado incluye variables ficticias (variables categóricas codificadas como 1 o 0) y variables ordinales segregadas de características de fecha como day_of_week o day_of_year.
         Las variables que se describen a continuación se utilizan como características para la construcción del modelo..""",
        manual_parameters=[param],
        responses={
            200: openapi.Response('Solicitud exitosa', CalendarSerializer),
            400: openapi.Response('Año incorrecto.'),
        }))
    def get(request, year):
        """Generacion de un calendario para un anio especifico

        - **parameters**::
              :param year:Anio para el cual el calendario va a ser generado
        - **return**::
              :return: Calendario con codigo de estado 200 (Solicitud exitosa).
        """
        logger.info("Obtener solicitud {}".format(year))
        if DateUtil.is_a_valid_year(year):
            if CalendarService.generate_calendar(year):
                calendar_list = Calendar.objects.all()
                calendar_serializer = CalendarSerializer(calendar_list, many=True).data
                return Response(calendar_serializer, status=status.HTTP_200_OK)
        else:
            return Response("Año antes de  " + str(settings.MINIMUM_YEAR) + " o Despues de  " +
                            str(settings.MAXIMUM_YEAR) + ".", status=status.HTTP_400_BAD_REQUEST)


class HolidayList(generics.GenericAPIView):
    """Clase para el manejo de los dias festivos
    """
    serializer_class = CalendarSerializer

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Devuelve todos los calendarios creados en la base de datos. Los calendarios almacenados incluyen dummy \
        variables (variables categóricas codificadas como 1 o 0) y variables ordinales segregadas de características de fecha \
        como day_of_week o day_of_year. \
        Las variables que se describen a continuación se utilizan como características para la construcción del modelo.""",
        responses={
            200: openapi.Response('Solicitud exitosa', CalendarSerializer),
        }))
    def get(request):
        """Obtiene la lista de los festivos utilizados como características para la construcción del modelo.

        - **parameters**::
              :param request:Peticion de festivos.
        - **return**::
              :return:entidad calendar_serializer con estado 200 (OK).
        """
        logger.info("get request holiday")
        holiday_list = Calendar.objects.all().filter(holiday=True)
        calendar_serializer = CalendarSerializer(holiday_list, many=True).data
        return Response(calendar_serializer, status=status.HTTP_200_OK)


class HolidayDetail(generics.GenericAPIView):
    """Clase para el manejo de los detalles  para los festivos.
    """
    serializer_class = CalendarSerializer
    param = openapi.Parameter('date', openapi.IN_PATH,
                              description="The date in format YYYY-MM-DD",
                              type=openapi.TYPE_STRING,
                              required=True)

    @staticmethod
    @method_decorator(decorator=swagger_auto_schema(
        operation_description="""Devuelve un detalle de fecha con todas las funciones del calendario. Las fechas almacenadas incluyen dummy \
        variables (variables categóricas codificadas como 1 o 0) y variables ordinales segregadas de características de fecha \
        como day_of_week o day_of_year. \
        Las variables que se describen a continuación se utilizan como características para la construcción del modelo.""",
        manual_parameters=[param],
        responses={
            200: openapi.Response('Solicitud exitosa.', CalendarSerializer),
            400: openapi.Response('Formato de fecha incorrecto'),
        }))
    def get(request, date):
        """Clase para el manejo de los detalles  para los festivos.
           """

        """Obtener los detalles para los festivos  para ser analizados       

        - **parameters**::
              :param request: Obtener todos los festivos 
              :param date: Festivo al cual se le va a obtener el detalle.
        - **return**::
              :return:Entidad calendar_serializer con estado 200 (OK).
        """
        logger.info("Obtener si es  festivo {}".format(date))
        if DateUtil.is_a_valid_date(date):
            date = DateUtil.validate_date(date)
            holiday = Calendar.objects.all().filter(date=date)
            calendar_serializer = CalendarSerializer(holiday, many=True).data
            return Response(calendar_serializer, status=status.HTTP_200_OK)
        else:
            return Response("Formato de fecha incorrecto", status=status.HTTP_400_BAD_REQUEST)
