"""
data_calendar.services.datemanagement.ColombianHolidays.py
==========================================================
Modulo para el manejo de los dias festivos

"""
from enum import Enum
import datetime


class EasterBasedHolidays(Enum):
    """Clase Enum para los festivos fijos en Colombia
    """
    DOMINGO_DE_RAMOS = -7
    JUEVES_SANTO = -3
    VIERNES_SANTO = -2
    PASCUA = 0
    ASCENCION_DE_JESUS = 43
    CORPUS_CHRISTI = 64
    SAGRADO_CORAZON_DE_JESUS = 71


class FixedHolidays(Enum):
    """Enum class para los festivos en Colombia
    """
    ANIO_NUEVO = datetime.datetime(1582, 1, 1).strftime("%m-%d")
    DIA_DEL_TRABAJO = datetime.datetime(1582, 5, 1).strftime("%m-%d")
    INDEPENDENCIA_COLOMBIA = datetime.datetime(1582, 7, 20).strftime("%m-%d")
    BATALLA_BOYACA = datetime.datetime(1582, 8, 7).strftime("%m-%d")
    INMACULADA_CONCEPCION = datetime.datetime(1582, 12, 8).strftime("%m-%d")
    NAVIDAD = datetime.datetime(1582, 12, 25).strftime("%m-%d")


class NonFixedHolidays(Enum):
    """Enum class para  los festivos colombianos no fijos
    """
    EPIFANIA_REYES_MAGOS = datetime.datetime(1582, 1, 6).strftime("%m-%d")
    SAN_JOSE = datetime.datetime(1582, 3, 19).strftime("%m-%d")
    SAN_PEDRO_Y_SAN_PABLO = datetime.datetime(1582, 6, 29).strftime("%m-%d")
    ASUNCION_DE_LA_VIRGEN = datetime.datetime(1582, 8, 15).strftime("%m-%d")
    DIA_DE_LA_RAZA = datetime.datetime(1582, 10, 12).strftime("%m-%d")
    DIA_DE_TODOS_LOS_SANTOS = datetime.datetime(1582, 11, 1).strftime("%m-%d")
    INDEPENDENCIA_CARTAGENA = datetime.datetime(1582, 11, 11).strftime("%m-%d")
