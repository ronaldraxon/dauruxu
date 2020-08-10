
from utilities.PandasUtilities import PandasUtilities as Pu
import logging

logger = logging.getLogger(__name__)


class DataStatisticsService:



    @staticmethod
    def generate_data_asset_profile_and_statistics(clean_data_asset):
        return Pu.create_json_pandas_profile(clean_data_asset)


    @staticmethod
    def extract_auto_correlated_variables(sorted_raw_data, value_field_name, variable_names):
        """
                - **parameters**::
                            :param sorted_raw_data:
                            :param value_field_name:
                            :param variable_names:
                - **return**::
                            :return:
        """
        corr_raw_data = sorted_raw_data
        variable_names.remove(value_field_name)
        corr_raw_data = corr_raw_data.drop(columns=variable_names)
        corr_matrix = corr_raw_data.corr()[value_field_name]
        corr_matrix = corr_matrix.sort_values(ascending=False)
        corr_values = corr_matrix.to_frame().iloc[2:8]
        cor_ind = corr_values.index.values
        cor_val = corr_values[value_field_name].values
        return cor_ind, cor_val