# Generated by Django 2.2.2 on 2020-02-08 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income_and_expense', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='expense',
            unique_together={('name', 'pay_date')},
        ),
        migrations.RemoveField(
            model_name='expense',
            name='period_date',
        ),
    ]
