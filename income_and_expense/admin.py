from django.contrib import admin

from .models import *

def unmark_undecided(modeladmin, request, queryset):
    queryset.update(undecided=False)
unmark_undecided.short_description = "Decided"

def mark_undecided(modeladmin, request, queryset):
    queryset.update(undecided=True)
mark_undecided.short_description = "Undecided"

def mark_done(modeladmin, request, queryset):
    queryset.update(done=True)
mark_done.short_description = "Done"

def unmark_done(modeladmin, request, queryset):
    queryset.update(done=False)
unmark_done.short_description = "No Done"

# Register your models here.


class DefaultExpenseMonthInline(admin.TabularInline):
    model = DefaultExpenseMonth
    extra = 12


class DefaultIncomeMonthInline(admin.TabularInline):
    model = DefaultIncomeMonth
    extra = 12


class AccountAdmin(admin.ModelAdmin):
    # チェンジリストページにどのフィールドを表示するか
    list_display = ('bank', 'user', 'balance')
    # どのフィールドにフィルタリングさせるか
    list_filter = ('bank', 'user')


class MethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'account')
    list_filter = ('account',)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'done', 'undecided', 'formed_amount',
        'method', 'account_info', 'pay_date', 'period_date'
    )
    list_filter = ('done', 'method', 'undecided')
    actions = [unmark_undecided, mark_undecided, mark_done, unmark_done]


class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'done', 'undecided', 'formed_amount',
        'method', 'account_info', 'pay_date'
    )
    list_filter = ('done', 'method', 'undecided')
    actions = [unmark_undecided, mark_undecided, mark_done, unmark_done]


class DefaultExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'undecided', 'formed_amount',
        'method', 'account_info', 'pay_day', 'period_day'
    )
    list_filter = ('method', 'undecided')
    inlines = [DefaultExpenseMonthInline]


class DefaultIncomeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'undecided', 'formed_amount',
        'method', 'account_info', 'pay_day'
    )
    list_filter = ('method', 'undecided')
    inlines = [DefaultIncomeMonthInline]


class DefaultExpenseMonthAdmin(admin.ModelAdmin):
    list_display = ('def_exp_name', 'month')
    list_filter = ('def_exp', 'month')


class DefaultIncomeMonthAdmin(admin.ModelAdmin):
    list_display = ('def_inc_name', 'month')
    list_filter = ('def_inc', 'month')


class SettlementAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'formed_balance')
    list_filter = ('year', 'month')


admin.site.register(Bank)
admin.site.register(User)
admin.site.register(Account, AccountAdmin)
admin.site.register(Method, MethodAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(DefaultExpense, DefaultExpenseAdmin)
admin.site.register(DefaultIncome, DefaultIncomeAdmin)
admin.site.register(DefaultExpenseMonth, DefaultExpenseMonthAdmin)
admin.site.register(DefaultIncomeMonth, DefaultIncomeMonthAdmin)
admin.site.register(Settlement, SettlementAdmin)
