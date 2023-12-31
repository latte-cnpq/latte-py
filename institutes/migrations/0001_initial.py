# Generated by Django 4.2.7 on 2023-11-12 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=255)),
                ('institute_code', models.CharField(blank=True, max_length=20, null=True)),
                ('country_acronym', models.CharField(blank=True, max_length=10, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
