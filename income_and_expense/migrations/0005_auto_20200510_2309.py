# Generated by Django 2.2.10 on 2020-05-10 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income_and_expense', '0004_auto_20200209_2358'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='expense',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='income',
            unique_together=set(),
        ),
    ]