# Generated by Django 4.0.4 on 2022-05-09 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_rename_loan_id_modifiedloan_offer_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modifiedloan',
            name='borrowing_user',
        ),
    ]
