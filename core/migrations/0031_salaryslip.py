# Generated by Django 4.0.4 on 2022-05-10 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0030_alter_profile_aadhaar_card_alter_profile_pan_card'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalarySlip',
            fields=[
                ('slip_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='salary_slip', verbose_name='Salary slip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
