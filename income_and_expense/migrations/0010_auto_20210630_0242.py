# Generated by Django 2.2.13 on 2021-06-29 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income_and_expense', '0009_auto_20210630_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateexpense',
            name='template_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
