# Generated by Django 3.0.3 on 2020-08-01 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model_trainer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forecastmodelrecord',
            name='code',
        ),
        migrations.AddField(
            model_name='forecastmodelrecord',
            name='code',
            field=models.CharField(db_index=True, help_text='<strong>The identifier which the training task is associated with.</strong>', max_length=256, null=True),
        ),
    ]