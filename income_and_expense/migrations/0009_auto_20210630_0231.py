# Generated by Django 2.2.13 on 2021-06-29 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income_and_expense', '0008_auto_20210629_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateexpense',
            name='template_name',
            field=models.CharField(default='default-name', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='templateexpense',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]