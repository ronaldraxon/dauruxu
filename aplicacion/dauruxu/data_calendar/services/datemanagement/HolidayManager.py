"""
data_calendar.services.datemanagement.HolidayManager.py
=======================================================
Modulo de gestion de las fechas
"""
from dateutil.relativedelta import relativedelta
from ..datemanagement import DateUtil
from ..datemanagement.Holiday import Holiday
from ..datemanagement.ColombianHolidays import EasterBasedHolidays, FixedHolidays, \
    NonFixedHolidays
import datetime


def get_pascua(date):
    """Obtener si la fecha es dia de pascua

        - **parameters**::
              :param date: Fecha para la cual se realiza la validacion
    """
    date = DateUtil.validate_date(date)
    year = date.year
    if year < 1583:
        return -1
    else:
        a = year % 19
        b = year >> 2
        c = b // 25 + 1
        d = (c * 3) >> 2
        e = ((a * 19) - ((c * 8 + 5) // 25) + d + 15) % 30
        e += (29578 - 1 - e * 32) >> 10
        e -= ((year % 7) + b - d + e + 2) % 7
        d = e >> 5
        day = e - d * 31
        month = d + 3
        date = datetime.date(year, month, day)
        description = EasterBasedHolidays.PASCUA.name
        return Holiday(date, description)


def get_domingo_de_ramos_date(date):
    """Obtiene si la fecha es domingo de ramos

        - **parameters**::
              :param date:fecha para la cual se le va a realizar la validacion
    """
    easter_date = get_pascua(date).date
    date = easter_date + relativedelta(days=EasterBasedHolidays.DOMINGO_DE_RAMOS.value)
    description = EasterBasedHolidays.DOMINGO_DE_RAMOS.name
    return Holiday(date, description)


def get_jueves_santo_date(date):
    """Obtiene si la fecha es Jueves santo

        - **parameters**::
              :param date:fecha para la cual se le va a realizar la validacion
    """

    easter_date = get_pascua(date).date
    date = easter_date + relativedelta(days=EasterBasedHolidays.JUEVES_SANTO.value)
    description = EasterBasedHolidays.JUEVES_SANTO.name
    return Holiday(date, description)


def get_viernes_santo_date(date):
    """Obtiene si la fecha es Viernes santo

          - **parameters**::
                :param date:fecha para la cual se le va a realizar la validacion
      """
    easter_date = get_pascua(date).date
    date = easter_date + relativedelta(days=EasterBasedHolidays.VIERNES_SANTO.value)
    description = EasterBasedHolidays.VIERNES_SANTO.name
    return Holiday(date, description)


def get_ascencion_de_jesus_date(date):
    """Obtiene si la fecha es del dia de ascencion de Jesus

        - **parameters**::
              :param date:fecha a la cual se le va a realizar la validacion
    """
    easter_date = get_pascua(date).date
    date = easter_date + relativedelta(days=EasterBasedHolidays.ASCENCION_DE_JESUS.value)
    description = EasterBasedHolidays.ASCENCION_DE_JESUS.name
    return Holiday(date, description)


def get_corpus_christi_date(date):
    """Obtiene si la fecha corresponde al dia del corphus christi

        - **parameters**::
              :param date:fecha a la cual se le va a realizar la validacion
    """
    easter_date = get_pascua(date).date
    date = easter_date + relativedelta(days=EasterBasedHolidays.CORPUS_CHRISTI.value)
    description = EasterBasedHolidays.CORPUS_CHRISTI.name
    return Holiday(date, description)


def get_sagrado_corazon_de_jesus_date(date):
    """Obtiene si la fecha corresponde al Sagrado Corazon de Jesus

        - **parameters**::
              :param date:fecha a la cual se le va a realizar la validacion
        - **return**::
              :return:
    """
    easter_date = get_pascua(date).date
    date = easter_date + relativedelta(days=EasterBasedHolidays.SAGRADO_CORAZON_DE_JESUS.value)
    description = EasterBasedHolidays.SAGRADO_CORAZON_DE_JESUS.name
    return Holiday(date, description)


def get_annio_nuevo(date):
    """Obtiene si la fecha corresponde a anio nuevo

        - **parameters**::
              :param date:fecha a la cual se le va a realizar la validacion
        - **return**::
              :return:
    """
    date = DateUtil.validate_date(date)
    date = str(date.year)+"-"+FixedHolidays.ANIO_NUEVO.value
    date = DateUtil.validate_date(date)
    description = FixedHolidays.ANIO_NUEVO.name
    return Holiday(date, description)


def get_dia_del_trabajo(date):
    """Obtiene si la fecha corresponde al dia del trabajo

            - **parameters**::
                  :param date:fecha a la cual se le va a realizar la validacion
        """
    date = DateUtil.validate_date(date)
    date = str(date.year)+"-"+FixedHolidays.DIA_DEL_TRABAJO.value
    date = DateUtil.validate_date(date)
    description = FixedHolidays.DIA_DEL_TRABAJO.name
    return Holiday(date, description)


def get_independencia_de_colombia(date):
    """Obtiene si la fecha corresponde al dia de la independencia

            - **parameters**::
                  :param date:fecha a la cual se le va a realizar la validacion
        """
    date = DateUtil.validate_date(date)
    date = str(date.year)+"-"+FixedHolidays.INDEPENDENCIA_COLOMBIA.value
    date = DateUtil.validate_date(date)
    description = FixedHolidays.INDEPENDENCIA_COLOMBIA.name
    return Holiday(date, description)


def get_batalla_de_boyaca(date):
    """Obtiene si la fecha corresponde al dia conmmemorativo a la batalla de boyaca

            - **parameters**::
                  :param date:fecha a la cual se le va a realizar la validacion
        """
    date = DateUtil.validate_date(date)
    date = str(date.year)+"-"+FixedHolidays.BATALLA_BOYACA.value
    date = DateUtil.validate_date(date)
    description = FixedHolidays.BATALLA_BOYACA.name
    return Holiday(date, description)


def get_inmaculada_concepcion(date):
    """Obtiene si la fecha corresponde al dia conmmemorativo a la inmmaculada concepcion

            - **parameters**::
                  :param date:fecha a la cual se le va a realizar la validacion
        """
    date = DateUtil.validate_date(date)
    date = str(date.year)+"-"+FixedHolidays.INMACULADA_CONCEPCION.value
    date = DateUtil.validate_date(date)
    description = FixedHolidays.INMACULADA_CONCEPCION.name
    return Holiday(date, description)


def get_navidad(date):
    """Obtiene si la fecha corresponde al dia conmmemorativo a la natividad

            - **parameters**::
                  :param date:fecha a la cual se le va a realizar la validacion
        """
    date = DateUtil.validate_date(date)
    date = str(date.year)+"-"+FixedHolidays.NAVIDAD.value
    date = DateUtil.validate_date(date)
    description = FixedHolidays.NAVIDAD.name
    return Holiday(date, description)


def get_epifania_reyes_magos_date(date):
    """Obtiene si la fecha corresponde al dia conmmemorativo a la epifania de los reyes magos
            - **parameters**::
                  :param date:fecha a la cual se le va a realizar la validacion
        """
    date = DateUtil.validate_date(date)
    reyes_magos = NonFixedHolidays.EPIFANIA_REYES_MAGOS.value
    reyes_magos = str(date.year)+"-"+reyes_magos
    date = DateUtil.shift_holiday_to_next_monday_if_not_monday(reyes_magos)
    description = NonFixedHolidays.EPIFANIA_REYES_MAGOS.name
    return Holiday(date, description)


def get_san_jose_date(date):
    """Obtiene si la fecha corresponde al dia conmmemorativo a la inmmaculada concepcion

            - **parameters**::
                  :param date:fecha a la cual se le va a realizar la validacion
        """
    date = DateUtil.validate_date(date)
    san_jose = NonFixedHolidays.SAN_JOSE.value
    san_jose = str(date.year)+"-"+san_jose
    date = DateUtil.shift_holiday_to_next_monday_if_not_monday(san_jose)
    description = NonFixedHolidays.SAN_JOSE.name
    return Holiday(date, description)


def get_san_pedro_y_san_pablo_date(date):
    """Obtiene si la fecha corresponde al dia conmmemorativo a san pedro y san pablo

            - **parameters**::
                  :param date:fecha a la cual se le va a realizar la validacion
        """
    date = DateUtil.validate_date(date)
    san_pedro_y_san_pablo = NonFixedHolidays.SAN_PEDRO_Y_SAN_PABLO.value
    san_pedro_y_san_pablo = str(date.year)+"-"+san_pedro_y_san_pablo
    date = DateUtil.shift_holiday_to_next_monday_if_not_monday(san_pedro_y_san_pablo)
    description = NonFixedHolidays.SAN_PEDRO_Y_SAN_PABLO.name
    return Holiday(date, description)


def get_asuncion_de_la_virgen_date(date):
    """Obtiene si la fecha corresponde al dia conmmemorativo a la asuncion de la virgen

            - **parameters**::
                  :param date:fecha a la cual se le va a realizar la validacion
        """
    date = DateUtil.validate_date(date)
    asuncion_de_la_virgen = NonFixedHolidays.ASUNCION_DE_LA_VIRGEN.value
    asuncion_de_la_virgen = str(date.year)+"-"+asuncion_de_la_virgen
    date = DateUtil.shift_holiday_to_next_monday_if_not_monday(asuncion_de_la_virgen)
    description = NonFixedHolidays.ASUNCION_DE_LA_VIRGEN.name
    return Holiday(date, description)


def get_dia_de_la_raza_date(date):
    """Obtiene si la fecha corresponde al dia conmmemorativo de la raza

               - **parameters**::
                     :param date:fecha a la cual se le va a realizar la validacion
           """
    date = DateUtil.validate_date(date)
    dia_de_la_raza = NonFixedHolidays.DIA_DE_LA_RAZA.value
    dia_de_la_raza = str(date.year)+"-"+dia_de_la_raza
    date = DateUtil.shift_holiday_to_next_monday_if_not_monday(dia_de_la_raza)
    description = NonFixedHolidays.DIA_DE_LA_RAZA.name
    return Holiday(date, description)


def get_dia_de_todos_los_santos_date(date):
    """Obtiene si la fecha corresponde al dia conmmemorativo de todos los santos

               - **parameters**::
                     :param date:fecha a la cual se le va a realizar la validacion
           """
    date = DateUtil.validate_date(date)
    dia_de_todos_los_santos = NonFixedHolidays.DIA_DE_TODOS_LOS_SANTOS.value
    dia_de_todos_los_santos = str(date.year)+"-"+dia_de_todos_los_santos
    date = DateUtil.shift_holiday_to_next_monday_if_not_monday(dia_de_todos_los_santos)
    description = NonFixedHolidays.DIA_DE_TODOS_LOS_SANTOS.name
    return Holiday(date, description)


def get_independencia_cartagena_date(date):
    """Obtiene si la fecha corresponde al dia conmmemorativo a la independencia de cartagena

               - **parameters**::
                     :param date:fecha a la cual se le va a realizar la validacion
           """
    date = DateUtil.validate_date(date)
    independencia_cartagena = NonFixedHolidays.INDEPENDENCIA_CARTAGENA.value
    independencia_cartagena = str(date.year)+"-"+independencia_cartagena
    date = DateUtil.shift_holiday_to_next_monday_if_not_monday(independencia_cartagena)
    description = NonFixedHolidays.INDEPENDENCIA_CARTAGENA.name
    return Holiday(date, description)


def get_list_of_holidays(date):
    """Obtiene todos los festivos colombianos

                - **parameters**::
                      :param date:fecha a la cual se le va a realizar la validacion
            """
    holiday_list = [
        get_domingo_de_ramos_date(date),
        get_jueves_santo_date(date),
        get_viernes_santo_date(date),
        get_pascua(date),
        get_ascencion_de_jesus_date(date),
        get_corpus_christi_date(date),
        get_sagrado_corazon_de_jesus_date(date),
        get_epifania_reyes_magos_date(date),
        get_san_jose_date(date),
        get_san_pedro_y_san_pablo_date(date),
        get_asuncion_de_la_virgen_date(date),
        get_dia_de_la_raza_date(date),
        get_dia_de_todos_los_santos_date(date),
        get_independencia_cartagena_date(date),
        get_annio_nuevo(date),
        get_dia_del_trabajo(date),
        get_independencia_de_colombia(date),
        get_batalla_de_boyaca(date),
        get_inmaculada_concepcion(date),
        get_navidad(date)
    ]
    return holiday_list


def is_holiday(date):
    """Obtiene si la fecha es festiva

                - **parameters**::
                      :param date:fecha a la cual se le va a realizar la validacion
            """
    date = DateUtil.validate_date(date)
    list_of_holidays = get_list_of_holidays(date)
    holiday = False
    for temp_date in list_of_holidays:
        if temp_date.date == date:
            holiday = True
    return holiday


def what_holiday_is(date):
    """Obtiene el tipo de festivo

                - **parameters**::
                      :param date:fecha a la cual se le va a realizar la validacion
            """
    date = DateUtil.validate_date(date)
    list_of_holidays = get_list_of_holidays(date)
    for temp_date in list_of_holidays:
        if temp_date.date == date:
            return temp_date.description


def is_business_day_with_saturday(date):
    """Get the day of date

        - **parameters**::
              :param date:
        - **return**::
              :return:
    """
    date = DateUtil.validate_date(date)
    if is_holiday(date) or date.weekday() == 6:
        return False
    else:
        return True


def is_business_day_without_saturday(date):
    """Get the day of date

        - **parameters**::
              :param date:
        - **return**::
              :return:
    """
    date = DateUtil.validate_date(date)
    if is_holiday(date) or date.weekday() == 5 or date.weekday() == 6:
        return False
    else:
        return True
