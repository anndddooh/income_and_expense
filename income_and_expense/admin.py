from django.contrib import admin

from .models import *

from income_and_expense.const import const_data

def unmark_undecided(modeladmin, request, queryset):
    queryset.update(undecided=False)
unmark_undecided.short_description = (
    const_data.const.SHOWN_NAME_DECIDED +
    const_data.const.SHOWN_NAME_CHANGE_TO
)

def mark_undecided(modeladmin, request, queryset):
    queryset.update(undecided=True)
mark_undecided.short_description = (
    const_data.const.SHOWN_NAME_UNDECIDED +
    const_data.const.SHOWN_NAME_CHANGE_TO
)

def mark_done(modeladmin, request, queryset):
    queryset.update(done=True)
mark_done.short_description = (
    const_data.const.SHOWN_NAME_DONE +
    const_data.const.SHOWN_NAME_CHANGE_TO
)

def unmark_done(modeladmin, request, queryset):
    queryset.update(done=False)
unmark_done.short_description = (
    const_data.const.SHOWN_NAME_NOT_DONE +
    const_data.const.SHOWN_NAME_CHANGE_TO
)

# Register your models here.


class DefaultExpenseMonthInline(admin.TabularInline):
    model = DefaultExpenseMonth
    extra = 12


class DefaultIncomeMonthInline(admin.TabularInline):
    model = DefaultIncomeMonth
    extra = 12


class AccountAdmin(admin.ModelAdmin):
    # チェンジリストページにどのフィールドを表示するか
    list_display = ('bank_custom', 'user_custom', 'formed_balance')
    # どのフィールドにフィルタリングさせるか
    list_filter = ('bank', 'user')

    def bank_custom(self, obj):
        return obj.bank

    def user_custom(self, obj):
        return obj.user

    # 表示名
    bank_custom.short_description = const_data.const.SHOWN_NAME_BANK
    user_custom.short_description = const_data.const.SHOWN_NAME_USER


class MethodAdmin(admin.ModelAdmin):
    list_display = ('name_custom', 'account_custom')
    list_filter = ('account',)

    def name_custom(self, obj):
        return obj.name

    def account_custom(self, obj):
        return obj.account

    name_custom.short_description = const_data.const.SHOWN_NAME_NAME
    account_custom.short_description = const_data.const.SHOWN_NAME_ACCOUNT


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'name_custom', 'done_custom', 'undecided_custom', 'formed_amount',
        'method_custom', 'account_info', 'pay_date_custom'
    )
    list_filter = ('done', 'method', 'undecided')
    actions = [unmark_undecided, mark_undecided, mark_done, unmark_done]

    def name_custom(self, obj):
        return obj.name

    def done_custom(self, obj):
        return obj.done

    def undecided_custom(self, obj):
        return obj.undecided

    def method_custom(self, obj):
        return obj.method

    def pay_date_custom(self, obj):
        return obj.pay_date

    name_custom.short_description = const_data.const.SHOWN_NAME_NAME
    done_custom.short_description = const_data.const.SHOWN_NAME_DONE
    undecided_custom.short_description = (
        const_data.const.SHOWN_NAME_UNDECIDED
    )
    method_custom.short_description = const_data.const.SHOWN_NAME_METHOD
    pay_date_custom.short_description = const_data.const.SHOWN_NAME_PAY_DATE


class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        'name_custom', 'done_custom', 'undecided_custom', 'formed_amount',
        'method_custom', 'account_info', 'pay_date_custom'
    )
    list_filter = ('done', 'method', 'undecided')
    actions = [unmark_undecided, mark_undecided, mark_done, unmark_done]

    def name_custom(self, obj):
        return obj.name

    def done_custom(self, obj):
        return obj.done

    def undecided_custom(self, obj):
        return obj.undecided

    def method_custom(self, obj):
        return obj.method

    def pay_date_custom(self, obj):
        return obj.pay_date

    name_custom.short_description = const_data.const.SHOWN_NAME_NAME
    done_custom.short_description = const_data.const.SHOWN_NAME_DONE
    undecided_custom.short_description = (
        const_data.const.SHOWN_NAME_UNDECIDED
    )
    method_custom.short_description = const_data.const.SHOWN_NAME_METHOD
    pay_date_custom.short_description = const_data.const.SHOWN_NAME_PAY_DATE


class DefaultExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'name_custom', 'undecided_custom', 'formed_amount',
        'method_custom', 'account_info', 'pay_day_custom'
    )
    list_filter = ('method', 'undecided')
    inlines = [DefaultExpenseMonthInline]

    def name_custom(self, obj):
        return obj.name

    def undecided_custom(self, obj):
        return obj.undecided

    def method_custom(self, obj):
        return obj.method

    def pay_day_custom(self, obj):
        return obj.pay_day

    name_custom.short_description = const_data.const.SHOWN_NAME_NAME
    undecided_custom.short_description = (
        const_data.const.SHOWN_NAME_UNDECIDED
    )
    method_custom.short_description = const_data.const.SHOWN_NAME_METHOD
    pay_day_custom.short_description = const_data.const.SHOWN_NAME_PAY_DAY


class DefaultIncomeAdmin(admin.ModelAdmin):
    list_display = (
        'name_custom', 'undecided_custom', 'formed_amount',
        'method_custom', 'account_info', 'pay_day_custom'
    )
    list_filter = ('method', 'undecided')
    inlines = [DefaultIncomeMonthInline]

    def name_custom(self, obj):
        return obj.name

    def undecided_custom(self, obj):
        return obj.undecided

    def method_custom(self, obj):
        return obj.method

    def pay_day_custom(self, obj):
        return obj.pay_day

    name_custom.short_description = const_data.const.SHOWN_NAME_NAME
    undecided_custom.short_description = (
        const_data.const.SHOWN_NAME_UNDECIDED
    )
    method_custom.short_description = const_data.const.SHOWN_NAME_METHOD
    pay_day_custom.short_description = const_data.const.SHOWN_NAME_PAY_DAY


class DefaultExpenseMonthAdmin(admin.ModelAdmin):
    list_display = ('def_exp_name', 'month_custom')
    list_filter = ('def_exp', 'month')

    def month_custom(self, obj):
        return obj.month

    month_custom.short_description = const_data.const.SHOWN_NAME_MONTH


class DefaultIncomeMonthAdmin(admin.ModelAdmin):
    list_display = ('def_inc_name', 'month_custom')
    list_filter = ('def_inc', 'month')

    def month_custom(self, obj):
        return obj.month

    month_custom.short_description = const_data.const.SHOWN_NAME_MONTH


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