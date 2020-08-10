"""
data_calendar.services.CalendarService.py
===============================
Modulo para el servicio de calendario
Administrador para  las fechas relevantes para los eventos
"""
from apps_administration.models.Property import PropertyKey
from apps_administration.services.PropertyService import PropertyService
from utilities.PandasUtilities import PandasUtilities
from utilities.NumpyUtilities import NumpyUtilities
from data_calendar.services.datemanagement import DateManager, HolidayManager, DateUtil
from data_calendar.models.Calendar import Calendar
from dateutil.relativedelta import relativedelta
from background_task import background
from background_task.models import Task
from utilities import TypeUtilities as Tu
import datetime
import datetime as dt
import pytz
import logging

logger = logging.getLogger(__name__)


class CalendarService:
    """Class para los metodos principales del calendarService
    """

    @staticmethod
    def generate_calendar(year):
        """Generar el calendario para el anio requerido

               - **parameters**::
                    :param year: Anio para el que se creara el calendario
               - **return**::
                    :return: Mensaje con el calendario del anio creado
        """
        logger.info("attempt to generate calendar for the year {}".format(year))
        db_date = Calendar.objects.all()
        if not db_date.filter(year=str(year)).exists():
            logger.info("generating calendar for the year {}".format(year))
            date = DateUtil.validate_date(str(year) + "-01" + "-01")
            for _ in range(DateManager.get_days_of_year(date)):
                day = DateManager.get_day_of_date(date)
                month = DateManager.get_month_of_date(date)
                year = DateManager.get_year_of_date(date)
                day_of_week = DateManager.get_weekday_of_date(date)
                day_of_week_nominal = Calendar.NominalDay(day_of_week).name
                day_of_year = DateManager.get_day_of_year_of_date(date)
                is_holiday = HolidayManager.is_holiday(date)
                coded_holiday = 1 if is_holiday else 0
                is_labor_day = DateManager.is_labor_day(day_of_week, is_holiday)
                coded_labor_day = 1 if is_labor_day else 0
                description = HolidayManager.what_holiday_is(date) if is_holiday else "N/A"
                Calendar(date=date, day=day, month=month, year=year, day_of_week=day_of_week, labor_day=is_labor_day,
                         coded_labor_day=coded_labor_day, day_of_week_nominal=day_of_week_nominal,
                         day_of_year=day_of_year,
                         holiday=is_holiday, coded_holiday=coded_holiday, description=description).save()
                date = date + relativedelta(days=1)
            return "Calendar for year {} has been created".format(year)
        else:
            logger.info("calendar for the year {} already exist on the database".format(year))
            return "Calendar for year {} already exist".format(year)

    @staticmethod
    def now_with_time_zone():
        """ Obtener  la fecha y hora actual de la zona horaria 'América / Bogotá'.

               - **return**::
                    :return: Fecha y hora actual
        """
        timezone = pytz.timezone("America/Bogota")
        return timezone.localize(dt.datetime.now())

    @staticmethod
    def now_without_time_zone():
        """Obtener fecha sin hora

               - **return**::
                    :return: Fecha actual.
        """
        return dt.date.today()

    @staticmethod
    @background(queue='calendar-managament-queue')
    def execute_task_generate_calendar():
        """Envio de la cola para peticion de generacion del calendario
        """
        year = dt.date.today().year
        CalendarService.generate_calendar(year + 1)

    @staticmethod
    def create_task_generate_calendar():
        """Creacion de la tarea en segundo plano para la generacion del calendario
        """
        year = CalendarService.now_with_time_zone().year
        begin_year = year - 5
        end_year = year + 2
        for i in range(begin_year, end_year):
            count = Calendar.objects.filter(year=i).count()
            if count == 0:
                CalendarService.generate_calendar(i)
        november = dt.datetime(year + 4, 11, 1, 0, 0, 0, 0, pytz.timezone("America/Los_Angeles"))
        pending_tasks_qs = Task.objects.filter(run_at__lte=november, queue='calendar-managament-queue').count()
        if pending_tasks_qs == 0:
            logger.info("Scheduling calendar process generate")
            CalendarService.execute_task_generate_calendar(schedule=november)

    @staticmethod
    def get_data_joined_with_calendar(raw_data, field_name):
        """ Combina calendario calendario con calendario sin procesar.

               - **parameters**::
                    :param raw_data:Datos sin procesar
                    :param field_name:Campo
        """

        CalendarService.build_necessary_calendars(raw_data, field_name)
        calendar_dates = Calendar.objects.filter(date__in=raw_data[field_name].values.tolist())
        calendar_dates_df = PandasUtilities.convert_django_query_set_to_pandas_data_frame(calendar_dates)
        complete_raw_data = PandasUtilities.join_pandas_data_frames_with_index(raw_data, calendar_dates_df, field_name)
        complete_raw_data = PandasUtilities.remove_caller_and_other_fields(complete_raw_data)
        return complete_raw_data

    @staticmethod
    def get_calendar_fields_with_data_frame(data_frame, date_field, fields_to_extract):
        """ Combines calendar calendar with raw calendar.

               - **parameters**::
                    :param data_frame:
                    :param date_field
                    :param fields_to_extract:
               - **return**::
                    :return:
        """
        data_frame = PandasUtilities.\
            convert_django_query_set_to_pandas_data_frame(Calendar.
                                                          objects.
                                                          filter(date__in=data_frame[date_field].values.tolist()))
        return data_frame[fields_to_extract]

    @staticmethod
    def get_maximum_date_allowed_with_boundary(today):
        """ Obtener la fecha maxima permitida
        - **parameters**::
                :param today:Dia para el cual se va a realizar la validacion
        """
        plus_date = today + \
                    dt.timedelta(days=int(PropertyService.retrieve_property_enum(PropertyKey.HIGH_BOUNDARY_DAY).value))
        return plus_date

    @staticmethod
    def get_time_delta_in_days(start_date, end_date):
        """Obtiene el delta en los dias
        - **parameters**::
                :param start_date:Fecha inicio para validacion
                :param end_date:Fecha fin para validacion
        """
        if isinstance(start_date, dt.date):
            d0 = start_date
        else:
            d0 = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, dt.date):
            d1 = end_date
        else:
            d1 = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
        delta = d1 - d0
        return delta.days

    @staticmethod
    def get_start_end_dates_from_ordered_data(data, field_name):
        data_start_date = data.iloc[0][field_name]
        data_end_date = data.iloc[-1][field_name]
        return data_start_date, data_end_date

    @staticmethod
    def get_years_sequence_from_dates(data_start_date, data_end_date):
        """Obtiene la secuencia de los anios a partir de un rango de fechas
        - **parameters**::
                :param start_date:Fecha inicio para validacion
                :param end_date:Fecha fin para validacion
        """
        start_year = int(str(data_start_date)[0:4])
        end_year = int(str(data_end_date)[0:4])
        return NumpyUtilities.generate_sequence_of_int_numbers(start_year, end_year, step=1, close_interval=True)

    @staticmethod
    def build_necessary_calendars(raw_data, field_name):
        """Construye los calendarios necesarios
             - **parameters**::
                     :param raw_data:Datos sin procesar
                     :param field_name:
             """
        raw_data_start_date, raw_data_end_date = CalendarService.get_start_end_dates_from_ordered_data(raw_data,
                                                                                                       field_name)
        years_sequence = CalendarService.get_years_sequence_from_dates(raw_data_start_date, raw_data_end_date)
        for year in years_sequence:
            if not Calendar.objects.filter(year=year).exists():
                CalendarService.generate_calendar(year)

    @staticmethod
    def get_1_day_before_date(date):
        yesterday = date - datetime.timedelta(days=1)
        return yesterday

    @staticmethod
    def get_available_calendar_fields():
        fields = Calendar._meta.fields
        field_names = list()
        for items in fields:
            field_names.append(str(items.name))
        return field_names

    @staticmethod
    def get_available_calendar_fields_as_choices():
        return Tu.tuple_from_list_and_remove_item(Calendar._meta.fields, 0)

