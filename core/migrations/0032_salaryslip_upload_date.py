# Generated by Django 4.0.4 on 2022-05-10 18:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_salaryslip'),
    ]

    operations = [
        migrations.AddField(
            model_name='salaryslip',
            name='upload_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
