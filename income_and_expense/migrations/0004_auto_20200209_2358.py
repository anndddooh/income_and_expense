# Generated by Django 2.2.2 on 2020-02-09 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income_and_expense', '0003_delete_settlement'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': '口座', 'verbose_name_plural': '口座'},
        ),
        migrations.AlterModelOptions(
            name='bank',
            options={'verbose_name': '銀行', 'verbose_name_plural': '銀行'},
        ),
        migrations.AlterModelOptions(
            name='defaultexpense',
            options={'verbose_name': '支出（デフォルト）', 'verbose_name_plural': '支出（デフォルト）'},
        ),
        migrations.AlterModelOptions(
            name='defaultexpensemonth',
            options={'verbose_name': '支出（デフォルト）適用月', 'verbose_name_plural': '支出（デフォルト）適用月'},
        ),
        migrations.AlterModelOptions(
            name='defaultincome',
            options={'verbose_name': '収入（デフォルト）', 'verbose_name_plural': '収入（デフォルト）'},
        ),
        migrations.AlterModelOptions(
            name='defaultincomemonth',
            options={'verbose_name': '収入（デフォルト）適用月', 'verbose_name_plural': '収入（デフォルト）適用月'},
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name': '支出', 'verbose_name_plural': '支出'},
        ),
        migrations.AlterModelOptions(
            name='income',
            options={'verbose_name': '収入', 'verbose_name_plural': '収入'},
        ),
        migrations.AlterModelOptions(
            name='method',
            options={'verbose_name': '支払方法', 'verbose_name_plural': '支払方法'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'ユーザー', 'verbose_name_plural': 'ユーザー'},
        ),
        migrations.RemoveField(
            model_name='defaultexpense',
            name='period_day',
        ),
    ]
