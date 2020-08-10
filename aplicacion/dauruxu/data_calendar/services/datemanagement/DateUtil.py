"""
data_calendar.services.datemanagement.DateUtil.py
============================================
Modulo para las utilidades de la fecha
"""
from dateutil.relativedelta import relativedelta
from ..datemanagement import HolidayManager
from django.conf import settings
import datetime


def is_a_valid_year(year):
    """Obtener si es un anio valido

        - **parameters**::
              :param year:Anio al cual se le va a realizar la validacion
        - **return**::
              :return:
    """
    return settings.MINIMUM_YEAR <= year <= settings.MAXIMUM_YEAR


def is_a_valid_date(date):
    """Obtener si es un dia valido

        - **parameters**::
              :param date:fecha a la cual se la va a realizar la validacion
    """
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_date(date):
    """Obtener si es una fecha valida

        - **parameters**::
              :param date:fecha a la cual se le va a realizar la validacion
    """
    if isinstance(date, datetime.date):
        return datetime.date(date.year, date.month, date.day)
    else:
        date = validate_date_length(date)
        date = validate_date_splitters(date)
        return validate_date_format(date)


def validate_date_length(date):
    """Validar tamanio del dia

        - **parameters**::
              :param date:Fecha a la cual se le va a realizar la validacion
    """
    if len(date) >= 10:
        return date[0:10]
    elif len(date) < 10:
        return -1


def validate_date_splitters(date):
    """Obtener los divisores de fecha

        - **parameters**::
              :param date:Fecha a la cual se le va a realizar la validacion
    """
    if date != -1:
        if date.find("/") > 1 or date.find("-") > 1:
            return date.replace("/", "-")
    return -1


def validate_date_format(date):
    """Obtener si la fecha tiene formato valido

        - **parameters**::
              :param date:fecha a la cual se le va  a realizar la validacion
    """
    if date != -1:
        if validate_date_format_year_month_day(date) == -1:
            if validate_date_format_day_month_year(date) == -1:
                return -1
            else:
                return validate_date_format_day_month_year(date)
        else:
            return validate_date_format_year_month_day(date)
    else:
        return -1


def validate_date_format_year_month_day(date):
    """Validar si el formato de fecha es el correcto YYYY/MM/DD

        - **parameters**::
              :param date:Fecha a la cual se le va a  realizar la validacion
    """
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        return datetime.date(date.year, date.month, date.day)
    except ValueError:
        return -1


def validate_date_format_day_month_year(date):
    """Validar formato para la fecha DD/MM/YYYYY

        - **parameters**::
              :param date:Fecha a la cual se le va a  realizar la validacion
    """
    try:
        date = datetime.datetime.strptime(date, '%d-%m-%Y')
        return datetime.date(date.year, date.month, date.day)
    except ValueError:
        return -1


def days_to_add(weekday):
    #TODO:TENERLO EN CUENTA
    """Get the day of date

        - **parameters**::
              :param weekday:
        - **return**::
              :return:
    """
    switcher = {
        1: 6,
        2: 5,
        3: 4,
        4: 3,
        5: 2,
        6: 1,
    }
    return switcher.get(weekday, 0)


def days_to_subtract(weekday):
    """Obtener dias a restar

        - **parameters**::
              :param weekday:Dia de la semana a la que se le va a realizar la validacion
    """
    switcher = {
        5: 1,
        6: 2,
        0: 3,
    }
    return switcher.get(weekday, 0)


def shift_holiday_to_next_monday_if_not_monday(date):
    """Cambiar el dia festivo al siguiente lunes , si este no es lunes

        - **parameters**::
              :param date:Fecha a la que se la va a realizar la validacion
    """
    date = validate_date(date)
    if date != -1:
        weekday = date.weekday()
        days = days_to_add(weekday)
        return date + relativedelta(days=days)
    else:
        return date


def shift_payday_to_previous_friday_if_weekend_or_holiday(date):
    """Cambiar el dia de pago al dia habil anterior si es festivo o fin de semana

        - **parameters**::
              :param date:Fecha a la que se le va a realizar la validacion
    """
    date = validate_date(date)
    weekday = date.weekday()
    if weekday == 0 and HolidayManager.is_holiday(date) is False:
        return 0
    else:
        days = days_to_subtract(weekday)
        return date - relativedelta(days=days)
