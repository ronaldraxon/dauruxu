"""
prediction_dispatcher.services.core.ModelExecutionService.py
============================================================
Modulo que compila los insumos de datos, procesamiento y modelo
y efectua el pronóstico con los valores originales de la
variable objetivo, dispuesto en el data_registry
"""
from apps_administration.models.Property import PropertyKey
from apps_administration.services.PropertyService import PropertyService
#from c4ufb_business.models.AtmClean import AtmCleanWithdrawalData
from data_preprocess.services.core.PreprocessRegistryService import PreprocessRegistryService
from data_preprocess.services.core.DataPreprocessReportService import DataPreprocessReportService
from utilities.PandasUtilities import PandasUtilities
from model_trainer.models.mt_storage.ForecastModelRecord import ForecastModel, ModelStatus
from prediction_dispatcher.models.storage.Prediction import Prediction
from data_preprocess.models.storage.DataAssetPreprocessReport import DataAssetPreprocessReport

from data_registry.models.storage.DataAsset import DataAsset
from prediction_dispatcher.models.storage.PredictionsHeader import PredictionsHeader
from django.conf import settings
import datetime
from datetime import date
import logging
import ast

logger = logging.getLogger(__name__)


class ModelExecutorService:
    """Main methods for the model executor service.
    """
    @staticmethod
    def create_atm_withdrawal_forecast_request(forecast_header_serializer):
        """
               - **parameters**::
                     :param forecast_header_serializer:
               - **return**::
                     :return:
        """
        logger.info("Attempting to create mt_core request")
        forecast_header = forecast_header_serializer.save()
        data_preprocess_report = DataPreprocessReportService.get_current_data_preprocess_report(forecast_header.code)
        forecast_header.observations = data_preprocess_report.data_management_observations
        forecast_header.save()
        logger.info("Starting the forecasting process for point {}".format(forecast_header.code))
        ModelExecutorService.forecast_atm_withdrawal_by_point_type(forecast_header.code,
                                                                   forecast_header.from_date,
                                                                   forecast_header.to_date,
                                                                   forecast_header)
        logger.info("The forecasting process for point {} was successfully ended".format(forecast_header.code))
        return forecast_header

    @staticmethod
    def forecast_atm_withdrawal_by_point_type(point_code, start_date, end_date, forecast_header):
        """

                - **parameters**::
                            :param point_code:
                            :param start_date:
                            :param end_date:
                            :param forecast_header:
        """
        target_field = PropertyKey.TARGET_ATM_WITHDRAW_FIELD.name

        model_withdraw, observations_w = ModelExecutorService.get_model_of_point(point_code, target_field)
        ModelExecutorService.set_observations_into_forecast_header(forecast_header, observations_w)
        start_balance = ModelExecutorService.get_previous_date_field_value(point_code, 'start_balance')
        end_balance = ModelExecutorService.get_previous_date_field_value(point_code, 'target_end_withdrawal_balance')
        ModelExecutorService.forecast_atm_withdrawal_values(point_code, start_date, end_date, forecast_header,
                                                            model_withdraw, start_balance, end_balance)

    @staticmethod
    def forecast_atm_withdrawal_values(point_code, start_date, end_date, forecast_header, model_withdraw,
                                       start_balance, end_balance):
        """

                - **parameters**::
                            :param point_code:
                            :param start_date:
                            :param end_date:
                            :param forecast_header:
                            :param withdraw_variable:
                            :param correlated_variables_w:
                            :param model_withdraw:
                            :param start_balance:
                            :param end_balance:
        """
        logger.info("Starting process of forecasting for atm with point's code {}".format(point_code))
        calendar_dates = ModelExecutorService.get_calendar_fields_with_date_range(start_date, end_date)

        for x in range(calendar_dates.shape[0]):
            calendar = calendar_dates.iloc[[x]]
            calendar_without_date = calendar.drop(['date'], axis=1)
            forecasting_inputs = ModelExecutorService. \
                    get_atm_withdrawal_forecast_inputs(start_balance, end_balance, calendar_without_date,
                                                       ModelExecutorService.get_input_variables(PropertyKey.INPUT_ATM_WITHDRAW_FIELDS.name))
            end_balance_forecast = ModelExecutorService.predict_with_linear_model_for_atm_withdrawal_and_get_array(model_withdraw.coefficients, model_withdraw.intercept, forecasting_inputs)
            complete_forecast = forecasting_inputs.copy()
            complete_forecast['target_end_withdrawal_balance'] = end_balance_forecast
            complete_forecast['total_consumption'] = complete_forecast['start_balance'] - complete_forecast['target_end_withdrawal_balance']
            start_balance = [complete_forecast['start_balance'].values]
            end_balance = [complete_forecast['target_end_withdrawal_balance'].values]
            complete_forecast = complete_forecast.astype('int64')
            Prediction.objects.create_new_forecast(calendar.date.values[0], complete_forecast.target_end_withdrawal_balance,
                                                   complete_forecast.total_consumption, forecast_header)



    @staticmethod
    def set_observations_into_forecast_header(forecast_header, mode_observation):
        """
                - **parameters**::
                            :param forecast_header:
                            :param withdraw_variable:
                            :param correlated_variables_w:

        """
        forecast_header.observations = forecast_header.observations + mode_observation
        forecast_header.save()

    @staticmethod
    def populate_atm_withdrawal_initial_regressors(start_balance, end_balance, calendar):
        """

                - **parameters**::
                            :param start_balance:
                            :param end_balance:
                            :param calendar:

                - **return**::
                            :return:
        """
        calendar = calendar.reset_index()
        d = {'start_balance_1day_before': start_balance[0], 'end_balance_1day_before': end_balance[0], 'start_balance': end_balance[0]}
        regressors_data_frame = PandasUtilities.create_data_frame(d)
        calendar = PandasUtilities.concat_pandas_data_frames([calendar, regressors_data_frame])
        return calendar

    @staticmethod
    def get_current_data_management(point_code):
        """

                - **parameters**::
                            :param point_code:
                - **return**::
                            :return:
        """
        data_management = DataAssetPreprocessReport.objects \
            .filter(point_code=point_code, is_the_current_data_management=True).first()
        return data_management

    @staticmethod
    def predict_with_linear_model_for_atm_withdrawal_and_get_array(coefficients, intercept, input_data):
        mult_data = input_data.multiply(other=coefficients)
        mult_data['inter'] = intercept[0]
        predictions = mult_data.sum(axis=1)
        return predictions.values

    @staticmethod
    def get_previous_date_field_value(point_code, required_field):
        """

                - **parameters**::
                            :param point_code:
                            :param date_field_in_clean_data:
                            :param required_field:
                - **return**::
                            :return:
        """
        clean_data = PreprocessRegistryService.get_date_ordered_and_bounded_atm_withdrawal_clean_data_by_point(point_code)
        clean_data = PandasUtilities.convert_django_query_set_to_pandas_data_frame(clean_data)
        date_field = PropertyService.retrieve_string_property_by_name(PropertyKey.DEFAULT_DATE_FIELD.name)
        clean_data = PandasUtilities.setting_index_and_sort_pandas_data_frame(clean_data, date_field)
        clean_data = clean_data[[required_field]]
        return clean_data.values

    @staticmethod
    def get_calendar_fields_with_date_range(start_date, end_date):
        """

                - **parameters**::
                            :param start_date:
                            :param end_date:
                - **return**::
                            :return:
        """
        calendar_dates = None
        #forecast_date_range = PandasUtilities.generate_pandas_date_range(start_date, end_date)
        #calendar_dates = Calendar.objects.filter(date__in=forecast_date_range.values.tolist())
        #calendar_dates = PandasUtilities.convert_django_query_set_to_pandas_data_frame(calendar_dates)
        #date_field = PropertyService.retrieve_string_property_by_name(PropertyKey.DEFAULT_DATE_FIELD.name)
        #calendar_dates = PandasUtilities.setting_index_and_sort_pandas_data_frame(calendar_dates, date_field)
        #calendar_dates = ModelExecutorService.get_atm_withdrawal_calendar_fields(calendar_dates)
        return calendar_dates

    @staticmethod
    def get_input_variables(input_variables_property):
        """

                - **parameters**::
                            :param input_variables_property:
                - **return**::
                            :return:
        """
        input_variables = PropertyService.retrieve_property_enum_by_key(input_variables_property).value
        input_variables = ast.literal_eval(input_variables)
        return input_variables

    @staticmethod
    def get_point_type(point_code):
        """

                - **parameters**::
                            :param point_code:
                - **return**::
                            :return:
        """
        logger.info("Getting type of point {}".format(point_code))
        point = DataAsset.objects.get(code=point_code)
        return point.type

    @staticmethod
    def get_values_from_clean_data_with_correlated_variables(clean_data, correlated_variables,
                                                             calendar_dates, minimum_day_shift):
        """

                - **parameters**::
                            :param clean_data:
                            :param correlated_variables:
                            :param calendar_dates:
                            :param minimum_day_shift:
                - **return**::
                            :return:
        """
        calendar = ModelExecutorService.get_calendar_fields(calendar_dates)
        withdraws = clean_data[['target_withdraw']]
        deposits = clean_data[['target_deposit']]
        number_of_rows = clean_data.shape[0]
        regressor_number = 1
        for value in correlated_variables:
            target_variable = value[:1]
            displacement_shift = int(value[2:])
            if target_variable == 'w':
                index_number = number_of_rows - displacement_shift
                regressor = withdraws.iloc[index_number:minimum_day_shift + index_number]
                regressor = regressor.reset_index()
                regressor = regressor[['target_withdraw']]
                regressor.columns = ['regressor' + str(regressor_number)]
                calendar = calendar.join(regressor)

            if target_variable == 'd':
                index_number = number_of_rows - displacement_shift
                regressor = deposits.iloc[index_number:minimum_day_shift + index_number]
                regressor = regressor.reset_index()
                regressor = regressor[['target_deposit']]
                regressor.columns = ['regressor' + str(regressor_number)]
                calendar = calendar.join(regressor)
            regressor_number = regressor_number + 1
        return calendar

    @staticmethod
    def get_calendar_fields(calendar_date):
        """

                - **parameters**::
                            :param calendar_date:
                - **return**::
                            :return:
        """
        calendar = calendar_date.reset_index()
        calendar = calendar.loc[:, ['day', 'month', 'day_of_week', 'coded_labor_day']]
        return calendar

    @staticmethod
    def get_atm_withdrawal_calendar_fields(calendar_date):
        """

                - **parameters**::
                            :param calendar_date:
                - **return**::
                            :return:
        """
        calendar = calendar_date.reset_index()
        calendar = calendar.loc[:, ['date', 'day', 'day_of_week', 'year']]
        return calendar

    @staticmethod
    def extract_minimum_shift_in_correlated_variables(correlated_vars):
        """

                - **parameters**::
                            :param correlated_vars:
                - **return**::
                            :return:
        """
        minimum = settings.HIGH_BOUNDARY_DAY
        for value in correlated_vars:
            candidate_number = int(value[2:])
            if candidate_number < minimum:
                minimum = candidate_number
        return minimum

    @staticmethod
    def get_model_of_point(point_code, target_field):
        """

                - **parameters**::
                            :param point_code:
                            :param target_field:
                - **return**::
                            :return:
        """
        logger.info("Retrieving model to predict variable {0} of point {1}".format(target_field, point_code))
        forecast_model = ForecastModel.objects.filter(status=ModelStatus.ACTIVE.name,
                                                      point_code=point_code,
                                                      variable_to_predict=target_field).first()
        if forecast_model is None:
            return None, " "
        else:
            observations = "Pearson correlation: " + str(forecast_model.test_r2) + "\n"
            observations = observations + "Model RMSE: " + str(forecast_model.test_rmse) + "\n"
            return forecast_model, observations

    @staticmethod
    def is_atm_withdrawal_clean_data_update(point_id):
        """

                - **parameters**::
                            :param point_id:
                - **return**::
                            :return:
        """
        today = date.today()
        yesterday = today - datetime.timedelta(days=1)
        #last_record = AtmCleanWithdrawalData.objects.filter(date=yesterday, point_id=point_id)
        last_record = True
        if last_record:
            return True
        else:
            return False

    @staticmethod
    def get_necessary_forecast_records_by_target(calendar_dates, forecast_collection, target_variable):
        """

                - **parameters**::
                            :param calendar_dates:
                            :param forecast_collection:
                            :param target_variable:
                - **return**::
                            :return:
        """
        forecast = PandasUtilities.convert_np_array_to_pandas_data_frame(forecast_collection, [target_variable])
        index = forecast_collection.shape[0] - calendar_dates.shape[0]
        return forecast.iloc[index:]

    @staticmethod
    def forecast_with_model_and_inputs(model, inputs):
        """
                - **parameters**::
                            :param model:
                            :param inputs:
                - **return**::
                            :return:
        """
        forecast = model.predict(inputs)
        return forecast.astype(int)

    @staticmethod
    def predict_with_linear_model_for_atm_withdrawal_and_get_array(coefficients, intercept, input_data):
        mult_data = input_data.multiply(other=coefficients)
        mult_data['inter'] = intercept[0]
        predictions = mult_data.sum(axis=1)
        return predictions.values

    @staticmethod
    def get_atm_withdrawal_forecast_inputs(start_balance, end_balance, calendar, set_variables):
        """
                - **parameters**::
                            :param start_balance:
                            :param end_balance:
                            :param correlated_variables:
                            :param calendar:
                            :param target_variable:
                            :param set_variables:
                - **return**::
                            :return:
        """
        forecast_inputs = ModelExecutorService.populate_atm_withdrawal_initial_regressors(start_balance, end_balance, calendar)
        forecast_inputs = forecast_inputs[set_variables]
        return forecast_inputs.astype('int64')

    @staticmethod
    def delete_forecast_records_by_point_code(code):
        PredictionsHeader.objects.filter(point_code=code).delete()
