# Generated by Django 2.2.17 on 2021-03-12 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('archived_at', models.DateTimeField(null=True)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField(verbose_name='Content')),
                ('required_type', models.CharField(choices=[('profile', 'Required to create a Profile'), ('optional', 'Optional')], default='optional', max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TermOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('archived_at', models.DateTimeField(null=True)),
                ('option_type', models.CharField(choices=[('agree', 'Agree'), ('decline', 'Decline'), ('unset', 'Unset')], max_length=40)),
                ('content', models.TextField(blank=True, verbose_name='Content')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='consents.Term')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Consent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('archived_at', models.DateTimeField(null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='consents.Term')),
                ('term_option', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='consents.TermOption')),
            ],
        ),
        migrations.AddConstraint(
            model_name='consent',
            constraint=models.UniqueConstraint(condition=models.Q(archived_at__isnull=True), fields=('person', 'term'), name='person__term__unique__when__archived_at__null'),
        ),
    ]
