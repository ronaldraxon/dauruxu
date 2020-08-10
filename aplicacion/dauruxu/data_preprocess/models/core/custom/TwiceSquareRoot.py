"""
data_preprocess.models.core.TwiceSquaredRoot.py
=============================================
Transformación que toma el valor de la variable
y extrae su raíz para luego multiplicarla por 2
"""

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from numpy import sqrt


class TwiceSquareRoot(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.columns = ""

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        self.columns = x.columns
        x_ = x.copy()
        x_ = 2 * sqrt(x_)
        return x_

    def inverse_transform(self, x):
        x_ = x.copy()
        x_ = x_ ** 2
        return x_

    def get_feature_names(self):
        return self.columns
