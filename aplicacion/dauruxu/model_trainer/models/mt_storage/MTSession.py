"""
model_trainer.models.MTSession.py
===================================
Registro de  puntos para controlar solicitudes
"""

from django.db import models
from django.utils.safestring import mark_safe


class MTSession(models.Model):

    code = models.CharField(db_index=True, primary_key=True, unique=True, max_length=100,
                            help_text=mark_safe("<strong>The code which the model is going to be"
                                                " associated with.</strong>"))
    clean_data = models.TextField(null=True, help_text=mark_safe("<strong>Clean data for further "
                                                                 "training and avoid additional request</strong>"))

    class Meta:
        """Clase para hacer referencia a la tabla asociada en la base de datos(point).
        """
        db_table = "mt_session"
