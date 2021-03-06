# Generated by Django 4.0.4 on 2022-05-30 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_portfoliorowtype_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='portfolio',
            options={'verbose_name': 'Portfolio', 'verbose_name_plural': 'Portfolio'},
        ),
        migrations.CreateModel(
            name='PortfolioVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=300)),
                ('portfolio', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.portfolio')),
            ],
        ),
    ]
