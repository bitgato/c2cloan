# Generated by Django 4.0.4 on 2022-05-09 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_loan_amount_alter_loan_interest_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='date_borrowing_start',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='date_lending_end',
            field=models.DateField(null=True),
        ),
    ]
