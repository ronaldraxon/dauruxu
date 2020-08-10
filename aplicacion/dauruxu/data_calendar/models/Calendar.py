"""
data_calendar.models.Calendar.py
================================
Modulo para la administracion de la entidad Calendario.
Marcado de fechas asociadas a los eventos generados por el usuario.
"""


from django.db import models
from django.utils.safestring import mark_safe
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.conf import settings
from enum import Enum


class Calendar(models.Model):
    """Esta clase muestra los campos que forman parte de la entidad Calendario
    """
    date = models.DateField(max_length=10, help_text=mark_safe("<strong>The  date in format YYYY-MM-DD.</strong>"))
    day = models.IntegerField(null=True, validators=[MaxValueValidator(31), MinValueValidator(1)],
                              help_text=mark_safe("<strong>Day number of the month.</strong>"))
    month = models.IntegerField(null=True, validators=[MaxValueValidator(12), MinValueValidator(1)],
                                help_text=mark_safe("<strong>Month number.</strong>"))
    year = models.IntegerField(null=True, validators=[MaxValueValidator(settings.MAXIMUM_YEAR),
                                                      MinValueValidator(settings.MINIMUM_YEAR)],
                               help_text=mark_safe("<strong>Year number.</strong>"))
    day_of_week = models.CharField(max_length=1, null=True, validators=[MaxValueValidator(12), MinValueValidator(1)],
                                   help_text=mark_safe("<strong>Day of week represented as number. 1 for Monday, "
                                                       "2 for Tuesday and so on.</strong>"))
    day_of_week_nominal = models.CharField(max_length=10, null=True,
                                           help_text=mark_safe("<strong>Day of week in nominal form.</strong>"))
    day_of_year = models.IntegerField(null=True, validators=[MaxValueValidator(366), MinValueValidator(1)],
                                      help_text=mark_safe("<strong>Day number of the year</strong>"))
    holiday = models.BooleanField(null=True, help_text=mark_safe("<strong>Logical value that represents whether"
                                                                 "a day is holiday or not.</strong>"))
    coded_holiday = models.SmallIntegerField(null=True, validators=[MaxValueValidator(1), MinValueValidator(0)],
                                             help_text=mark_safe("<strong>Coded value that represents whether"
                                                                 "a day is holiday or not.</strong>"))
    labor_day = models.BooleanField(null=True, help_text=mark_safe("<strong>Logical value that represents whether"
                                                                   "a day is labor day or not. A labor day is "
                                                                   "considered as a day of the week different to"
                                                                   "weekends or holidays.</strong>"))
    coded_labor_day = models.SmallIntegerField(null=True, validators=[MaxValueValidator(1), MinValueValidator(0)],
                                               help_text=mark_safe("<strong>Coded value that represents whether"
                                                                   "a day is labor day or not. A labor day is "
                                                                   "considered as a day of the week different to "
                                                                   "weekends or holidays.</strong>"))
    description = models.CharField(max_length=100, help_text=mark_safe("<strong>Description of the holiday or "
                                                                       "celebration is considered for "
                                                                       "that day.</strong>"))

    class NominalDay(Enum):
        """Esta clase es para enumerar los 7 dias de la semana.
        """
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    class Meta:
        """Clase para hacer referencia a la tabla asociada en la base de datos (calendar).
        """
        db_table = "dc_calendar"
