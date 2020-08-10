from pandas_profiling import ProfileReport
import pandas as pd
import numpy as np


class PandasUtilities:

    @staticmethod
    def convert_json_string_to_pandas_data_frame(json_string):
        return pd.read_json(json_string)

    @staticmethod
    def convert_list_of_dict_to_pandas_data_frame(list_of_dict):
        return pd.DataFrame(list_of_dict)

    @staticmethod
    def convert_np_array_to_pandas_data_frame(np_array, columns_names):
        return pd.DataFrame(data=np_array, columns=columns_names)

    @staticmethod
    def convert_django_query_set_to_pandas_data_frame(query_set):
        return pd.DataFrame(query_set.values())

    @staticmethod
    def setting_index_and_sort_pandas_data_frame(pandas_data_frame, index_name):
        pandas_data_frame = pandas_data_frame.set_index(keys=index_name)
        pandas_data_frame = pandas_data_frame.sort_values(by=index_name)
        pandas_data_frame = pandas_data_frame.reset_index()
        return pandas_data_frame

    @staticmethod
    def get_missing_dates_from_pandas_data_frame(pandas_data_frame, date_column_name):
        number_of_days = len(pandas_data_frame[date_column_name])
        return pd.date_range(start=pandas_data_frame.iloc[0][date_column_name],
                             end=pandas_data_frame.iloc[number_of_days - 1][date_column_name])\
                 .difference(pandas_data_frame[date_column_name])

    @staticmethod
    def remove_index_from_pandas_data_frame(pandas_data_frame):
        return pandas_data_frame.reset_index()

    @staticmethod
    def get_general_statistics(pandas_data_frame):
        pandas_data_frame = pd.to_numeric(pandas_data_frame)
        return pandas_data_frame.describe()

    @staticmethod
    def get_mode(pandas_data_frame):
        return pandas_data_frame.mode()

    @staticmethod
    def get_median(pandas_data_frame):
        return pandas_data_frame.median()

    @staticmethod
    def get_kurtosis(pandas_data_frame):
        return pandas_data_frame.kurtosis()

    @staticmethod
    def get_skew(pandas_data_frame):
        return pandas_data_frame.skew()

    @staticmethod
    def get_iqr(quant25, quant75):
        return quant75 - quant25

    @staticmethod
    def get_lower_boudary(quant25, iqr):
        return quant25 - 1.5 * iqr

    @staticmethod
    def get_higher_boudary(quant75, iqr):
        return quant75 + 1.5 * iqr

    @staticmethod
    def count_lower_boudary_outliers(pandas_data_frame, lower_boundary):
        return len(pandas_data_frame[(pandas_data_frame < lower_boundary)])

    @staticmethod
    def count_higher_boudary_outliers(pandas_data_frame, higher_boundary):
        return len(pandas_data_frame[(pandas_data_frame > higher_boundary)])

    @staticmethod
    def count_zero_values(pandas_data_frame):
        return len(pandas_data_frame[(pandas_data_frame == 0)])

    @staticmethod
    def replace_zero_values_with_field_value(pandas_data_frame, field_to_replace, field_value):
        pandas_data_frame[field_to_replace] = np.where(pandas_data_frame[field_to_replace] == 0,
                                                       pandas_data_frame[field_value],
                                                       pandas_data_frame[field_to_replace])
        return pandas_data_frame

    @staticmethod
    def generate_pandas_date_range(from_date, to_date):
        return pd.date_range(start=from_date, end=to_date).strftime('%Y-%m-%d')

    @staticmethod
    def join_pandas_data_frames(left_df, right_df, left_on_field, right_on_field):
        joined = pd.merge(left=left_df, right=right_df, left_on=left_on_field, right_on=right_on_field)
        return joined

    @staticmethod
    def join_pandas_data_frames_with_index(left_df, right_df, index_name):
        return left_df.set_index(index_name).join(right_df.set_index(index_name),
                                                  lsuffix='_caller', rsuffix='_other')

    @staticmethod
    def remove_caller_and_other_fields(data_frame):
        data_frame = data_frame.ix[:, ~data_frame.columns.str.contains('_caller$')]
        data_frame = data_frame.ix[:, ~data_frame.columns.str.contains('_other$')]
        return data_frame

    @staticmethod
    def rebuild_pandas_data_frames(data):
        data_frame = pd.DataFrame(data)
        return data_frame

    @staticmethod
    def convert_numpy_float_array_to_int_data_frame(data, field_name):
        data = data.astype(int)
        return PandasUtilities.convert_np_array_to_pandas_data_frame(data, field_name)

    @staticmethod
    def convert_list_to_data_frame(data, field_name):
        return pd.DataFrame(data, columns=[field_name])

    @staticmethod
    def create_data_frame(data):
        return pd.DataFrame(data)

    @staticmethod
    def set_pandas_data_frame_index(data, index):
        return data.set_index(keys=index)

    @staticmethod
    def join_pandas_data_frame_and_index_array(data_collection, index_array):
        return data_collection.set_index(index_array)

    @staticmethod
    def join_pandas_data_frame_and_index_array_with_keyname(data_collection, index_array, index_name):
        data_collection = data_collection.set_index(index_array)
        data_collection.index.name = index_name
        return data_collection

    @staticmethod
    def sort_pandas_data_frame_by_index(data, index):
        return data.sort_values(by=index)

    @staticmethod
    def pandas_df_to_excel(data_frame, file_name):
        data_frame.to_excel(file_name)

    @staticmethod
    def create_pandas_df_from_single_value(value):
        np.array(value)
        pd.DataFrame(value)

    @staticmethod
    def read_csv_to_pandas_data_frame(path, separator):
        return pd.read_csv(path, sep=separator)

    @staticmethod
    def concat_pandas_data_frames(data_frames):
        return pd.concat(data_frames, axis=1, sort=False)

    @staticmethod
    def create_json_pandas_profile(title, data):
        profile = ProfileReport(data, title=title)
        return profile.to_json()
