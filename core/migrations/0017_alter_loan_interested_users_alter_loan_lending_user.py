# Generated by Django 4.0.4 on 2022-05-09 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0016_alter_loan_date_borrowing_start_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='interested_users',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loan',
            name='lending_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_lending', to=settings.AUTH_USER_MODEL),
        ),
    ]