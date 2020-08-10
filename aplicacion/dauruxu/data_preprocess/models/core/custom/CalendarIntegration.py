"""
data_preprocess.models.core.custom.CalendarIntegration.py
=========================================================
Transformación que toma el primer campo de un dataframe y lo envía
como parámetro  una consulta de fechas. El formato de los valores
de fecha en el campo deben ser YYYY-MM-DD. Como parámetro recive una lista
de los campos que se desean extraer del servicio de calendarios
"""

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from data_calendar.services.CalendarService import CalendarService as Cs


class CalendarIntegration(TransformerMixin, BaseEstimator):

    def __init__(self, calendar_fields=None):
        self.calendar_fields = calendar_fields

    def fit(self, x=None, y=None):
        return self

    def transform(self, x):
        return Cs.get_calendar_fields_with_data_frame(x, list(x.columns)[0], self.calendar_fields)

    def get_feature_names(self):
        return self.calendar_fields

