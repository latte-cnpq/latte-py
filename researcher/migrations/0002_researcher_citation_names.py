# Generated by Django 4.2.7 on 2023-11-13 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researcher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='researcher',
            name='citation_names',
            field=models.TextField(blank=True, null=True),
        ),
    ]
