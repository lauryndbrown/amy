# Generated by Django 2.2.10 on 2020-02-23 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoemails', '0008_auto_20200218_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trigger',
            name='action',
            field=models.CharField(choices=[('new-instructor', 'Instructor is added to the workshop'), ('week-after-workshop-completion', '7 days past the end date of an active workshop'), ('self-organised-request-form', 'A new event is created from Self-Organised Request Form')], max_length=50, verbose_name='Action'),
        ),
    ]
