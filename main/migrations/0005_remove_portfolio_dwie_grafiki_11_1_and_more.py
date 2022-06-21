# Generated by Django 4.0.4 on 2022-05-28 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_dwie_grafiki_11_portfolio_dwie_grafiki_11_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='dwie_grafiki_11_1',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='dwie_grafiki_11_2',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='dwie_grafiki_12_1',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='dwie_grafiki_12_2',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='dwie_grafiki_21_1',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='dwie_grafiki_21_2',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='grafika_fw',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='grafika_mobilna_fw',
        ),
        migrations.CreateModel(
            name='PortfolioRowType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=60)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='main.portfoliorowtype')),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioRow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo1', models.FileField(blank=True, upload_to='')),
                ('photo2', models.FileField(blank=True, upload_to='')),
                ('portfolio', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.portfolio')),
                ('portfolioRowType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.portfoliorowtype')),
            ],
        ),
    ]
