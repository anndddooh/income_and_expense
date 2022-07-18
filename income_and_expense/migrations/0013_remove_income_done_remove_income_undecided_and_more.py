# Generated by Django 4.0.6 on 2022-07-18 14:05

from django.db import migrations, models


def apply_state_settings(apps, schema_editor):
    # Incomeモデルを取得
    Income = apps.get_model('income_and_expense', 'Income')

    for income in Income.objects.all():
        if income.undecided == True:
            income.state = 1
        elif income.done == False:
            income.state = 2
        else:
            income.state = 3
        income.save()


class Migration(migrations.Migration):

    dependencies = [
        ('income_and_expense', '0012_remove_expense_done_remove_expense_undecided_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='state',
            field=models.IntegerField(choices=[(1, '未定'), (2, '確定'), (3, '完了')], default=1),
        ),
        migrations.RunPython(apply_state_settings, None),
        migrations.RemoveField(
            model_name='income',
            name='done',
        ),
        migrations.RemoveField(
            model_name='income',
            name='undecided',
        )
    ]
