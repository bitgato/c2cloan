# Generated by Django 4.0.4 on 2022-05-09 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_profile_aadhaar_card_alter_profile_pan_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='date_applied',
            field=models.DateField(auto_now_add=True),
        ),
    ]
