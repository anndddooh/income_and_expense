# Generated by Django 4.0.6 on 2022-07-18 06:40

from django.db import migrations, models


def apply_state_settings(apps, schema_editor):
    # Expenseモデルを取得
    Expense = apps.get_model('income_and_expense', 'Expense')

    for expense in Expense.objects.all():
        if expense.undecided == True:
            expense.state = 0
        elif expense.done == False:
            expense.state = 1
        else:
            expense.state = 2
        expense.save()


class Migration(migrations.Migration):

    dependencies = [
        ('income_and_expense', '0011_loan'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='state',
            field=models.IntegerField(choices=[(0, '未定'), (1, '確定'), (2, '完了')], default=1),
        ),
        migrations.RunPython(apply_state_settings, None),
        migrations.RemoveField(
            model_name='expense',
            name='done',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='undecided',
        )
    ]