"""
data_preprocess.models.core.custom.CMinMaxScaler.py
=========================================================
Realiza escalamiento min max con la implementación de nombres de campos
"""

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.preprocessing import MinMaxScaler


class CMinMaxScaler(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.columns = None
        self.transformer = MinMaxScaler()
        pass

    def fit(self, x):
        self.transformer.fit(x)
        return self

    def transform(self, x):
        self.columns = x.columns
        return self.transformer.transform(x)

    def get_feature_names(self):
        return self.columns
