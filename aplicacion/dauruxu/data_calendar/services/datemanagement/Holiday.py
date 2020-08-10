"""
data_calendar.services.datemanagement.Holiday.py
================================================
Modulo de manejo de los dias festivos
"""


class Holiday:
    """Clase de los dias festivos
    """

    def __init__(self, date, description):
        self.date = date
        self.description = description
