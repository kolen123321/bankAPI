# Generated by Django 3.1.1 on 2021-09-20 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_api_v1', '0003_auto_20210920_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='financeprofile',
            name='title',
            field=models.CharField(default='', max_length=32),
        ),
    ]
