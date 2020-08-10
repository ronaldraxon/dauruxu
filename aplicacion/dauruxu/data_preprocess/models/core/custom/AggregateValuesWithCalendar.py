"""
data_preprocess.models.core.custom.AggregateValuesWithCalendar.py
=========================================================
Realiza una integración de un campo de fecha y lo toma como referencia
para realizar la agrupación con un segundo campo de valores.
Los campos seleccionados para esta transformación deben ir en el siguiente orden: Campo_fecha, campo_valores.
El campo extraído de la integración y por el cual se hará la integración deberá ingresar como parámetro
de esta tranformación: aggregation_field
"""

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin


class AggregateValesWithCalendar(BaseEstimator,TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x=None):
        pass

    def transform(self, x):
        pass

    def get_feature_names(self):
        pass
