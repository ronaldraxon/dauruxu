"""
data_calendar.urls.py
=====================
Modulo para la administracion de las url necesarias para este calendario
"""

from django.urls import path

from data_calendar.views.CalendarView import CalendarGeneration , HolidayDetail , HolidayList


app_name = "data_calendar"
urlpatterns = [
                path("api/calendar/generation/<int:year>", CalendarGeneration.as_view(), name="calendar_generation"),
                path("api/calendar/holiday/<str:date>", HolidayDetail.as_view(), name="holiday_detail"),
                path("api/calendar/holiday/", HolidayList.as_view(), name="holiday_list"),
              ]
