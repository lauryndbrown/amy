# Generated by Django 2.2.5 on 2019-12-18 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoemails', '0004_auto_20191128_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='rqjob',
            name='scheduled_execution',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Scheduled execution time', help_text='Set automatically when scheduling an email.'),
        ),
    ]