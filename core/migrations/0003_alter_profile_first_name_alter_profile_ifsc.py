# Generated by Django 4.0.4 on 2022-05-08 18:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_profile_aadhaar_card_alter_profile_acc_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ifsc',
            field=models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11)], verbose_name='IFSC Code'),
        ),
    ]
