# Generated by Django 4.0.6 on 2022-07-24 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income_and_expense', '0014_remove_defaultexpense_undecided_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='memo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='memo',
            field=models.TextField(blank=True, null=True),
        ),
    ]