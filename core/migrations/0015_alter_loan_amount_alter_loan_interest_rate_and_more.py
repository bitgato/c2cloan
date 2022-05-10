# Generated by Django 4.0.4 on 2022-05-09 08:45

import core.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_loan_tenure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='Amount required'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='interest_rate',
            field=models.FloatField(validators=[core.models.interest_rate], verbose_name='Interest rate'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='tenure',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(12)], verbose_name='Tenure (in months)'),
        ),
    ]