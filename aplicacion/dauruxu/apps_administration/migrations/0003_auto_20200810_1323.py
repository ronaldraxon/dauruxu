# Generated by Django 3.0.3 on 2020-08-10 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_administration', '0002_auto_20200805_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='type',
            field=models.CharField(choices=[('APP_ADMIN', 'APP_ADMIN'), ('DATA_REGISTRY', 'DATA_REGISTRY'), ('DATA_PREPROCESS', 'DATA_PREPROCESS'), ('MODEL_TRAINER', 'MODEL_TRAINER'), ('DATA_CALENDAR', 'DATA_CALENDAR'), ('PREDICTION_DISPATCHER', 'PREDICTION_DISPATCHER')], default='APP_ADMIN', help_text='<strong>The type of the property.</strong>', max_length=25),
        ),
    ]