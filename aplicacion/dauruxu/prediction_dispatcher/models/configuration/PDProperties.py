"""
prediction_dispatcher.models.configuration.PDPropertiesService.py
=================================================================
Modulo para el singleton de  propiedades del prediction_dispatcher. Esta clase evita varias que se envien varias solicitudes a
apps_administration por propiedades de la aplicacion
"""


class FDProperties(object):

    instance = None

    class __MEProperties:
        def __init__(self):
            self.LOW_BOUNDARY_DAY = 1
            self.HIGH_BOUNDARY_DAY = 31
            self.ENABLE_PREDICTION_STORING = True

        def __str__(self):
            return '{0!r}'.format(self)

        def update_property_values(self, properties):
            self.LOW_BOUNDARY_DAY = int(properties.loc['LOW_BOUNDARY_DAY'].value)
            self.HIGH_BOUNDARY_DAY = int(properties.loc['HIGH_BOUNDARY_DAY'].value)
            self.ENABLE_PREDICTION_STORING = bool(properties.loc['ENABLE_PREDICTION_STORING'].value)

    def __new__(cls):
        if not FDProperties.instance:
            FDProperties.instance = FDProperties.__MEProperties()
        return FDProperties.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, **kwargs):
        return setattr(self.instance, name)
