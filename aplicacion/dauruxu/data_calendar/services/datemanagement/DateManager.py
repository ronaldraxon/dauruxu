"""
data_calendar.services.datemanagement.DateManager.py
====================================================
Modelo para el data Manager
"""
from dateutil.relativedelta import relativedelta
from ..datemanagement import DateUtil
import datetime
import calendar


def get_day_of_date(date):
    """Obtener el dia de la fecha
        - **parameters**::
              :param date:fecha a la que se le va a obtener el dia
    """
    date = DateUtil.validate_date(date)
    return date if date == -1 else date.day


def get_month_of_date(date):
    """Obtener el mes de la fecha

        - **parameters**::
              :param date:fecha a la que se le va a obtener el mes
    """
    date = DateUtil.validate_date(date)
    return date if date == -1 else date.month


def get_year_of_date(date):
    """Obtener anio de la fecha

        - **parameters**::
              :param date:fecha a la que se le va a obtener el anio
    """
    date = DateUtil.validate_date(date)
    return date if date == -1 else date.year


def get_weekday_of_date(date):
    """Obtener el dia de la semana

        - **parameters**::
              :param date:fecha a la que se le va a obtener el dia de la semana
    """
    date = DateUtil.validate_date(date)
    return date if date == -1 else date.isoweekday()


def get_day_of_year_of_date(date):
    """Obtener el dia del anio

        - **parameters**::
              :param date:fecha a la que se le va a obtener el dia del anio
    """
    date = DateUtil.validate_date(date)
    return date.strftime('%j')


def get_days_of_year(date):
    """Obtener los dias del anio

        - **parameters**::
              :param date:fecha a la cual se le van a obtener los dias del anio
    """
    return 366 if is_leap_year(date) else 365


def is_leap_year(date):
    year = get_year_of_date(date)
    return year if year == -1 else (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def is_weekend(day_of_week):
    """Valida si es fin de semana
         - **parameters**::
               :param day_of_week:dia apara el cual se va a determinar si es un fin de semana
     """
    if day_of_week == 6 or day_of_week == 7:
        return True
    else:
        return False


def is_labor_day(day_of_week, is_holyday):
    """Valida si es un dia laborable
           - **parameters**::
                 :param day_of_week:indica el dia la semana
                 :param is_holyday:indica si es un dia festivo
       """
    if is_weekend(day_of_week) or is_holyday:
        return False
    else:
        return True


def get_days_since_previous_fortnight_of_date(date):
    """obtener dias desde la quincena anterior a la fecha
           - **parameters**::
                 :param date:fecha a la que se le va a realizar la validacion
       """
    date = DateUtil.validate_date(date)
    if date != -1:
        if date.day <= 15:
            previous_fortnight = datetime.date(date.year, date.month, 1)
            previous_fortnight = previous_fortnight - relativedelta(days=1)
            previous_fortnight = date - previous_fortnight
            return previous_fortnight.days
        else:
            previous_fortnight = datetime.date(date.year, date.month, 15)
            previous_fortnight = date - previous_fortnight
            return previous_fortnight.days
    else:
        return date


def get_days_to_next_fortnight_of_date(date):
    """obtener dias hasta la siguiente quincena de la fecha
           - **parameters**::
                 :param date:fecha a la que se le va a realizar la validacion
       """
    date = DateUtil.validate_date(date)
    if date != -1:
        if date.day < 15:
            next_fortnight = datetime.date(date.year, date.month, 15)
            next_fortnight = next_fortnight - date
            return next_fortnight.days
        else:
            next_fortnight = calendar.monthrange(date.year, date.month)[1]
            if date.day == next_fortnight:
                next_fortnight = date
                next_fortnight = next_fortnight + relativedelta(days=15)
                next_fortnight = datetime.date(next_fortnight.year, next_fortnight.month, next_fortnight.day)
                next_fortnight = next_fortnight - date
                return next_fortnight.days
            else:
                next_fortnight = date
                next_fortnight = next_fortnight - date
                return next_fortnight.days
    else:
        return date


def get_payday_of_previous_fortnight(date):
    """obtener dia de pago de la quincena anterior
           - **parameters**::
                 :param date:fecha a la que se le va a realizar la validacion
       """
    date = DateUtil.validate_date(date)
    days_since_previous_fortnight = get_days_since_previous_fortnight_of_date(date)
    previous_fortnight = date
    previous_fortnight = previous_fortnight - relativedelta(days=days_since_previous_fortnight)
    previous_fortnight = DateUtil.shift_payday_to_previous_friday_if_weekend_or_holiday(previous_fortnight)
    previous_fortnight = date - previous_fortnight
    return previous_fortnight.days


def get_payday_of_next_fortnight(date):
    """obtener dia de pago de la siguiente quincena
           - **parameters**::
                 :param date:fecha a la que se le va a realizar la validacion
       """
    date = DateUtil.validate_date(date)
    days_to_next_fortnight = get_days_to_next_fortnight_of_date(date)
    next_fortnight = date
    next_fortnight = next_fortnight + relativedelta(days=days_to_next_fortnight)
    next_fortnight = DateUtil.shift_payday_to_previous_friday_if_weekend_or_holiday(next_fortnight)
    next_fortnight = next_fortnight - date
    return next_fortnight.days
