# Generated by Django 4.0.4 on 2022-05-28 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_portfolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='link',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
