# Generated by Django 4.0.4 on 2022-05-09 16:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_rename_new_interest_rate_modifiedloan_interest_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='tenure',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Tenure (in months)'),
        ),
        migrations.AlterField(
            model_name='modifiedloan',
            name='tenure',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='New Tenure (in months)'),
        ),
    ]
