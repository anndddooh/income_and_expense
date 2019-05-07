import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum
from cerberus import Validator
from dateutil.relativedelta import relativedelta

from .models import Expense, Income, DefaultExpenseMonth, DefaultIncomeMonth, Settlement, Account
from .forms import IncomeFormSet

MIN_YEAR = 2019
MAX_YEAR = 2020
MIN_MONTH = 1
MAX_MONTH = 12
FIRST_DAY = 28 # 各月の会計開始日
MIN_1ST_DAY_AS_NEXT_MONTH = 16 # 翌月に計上する会計開始日の最小値
"""
例)
・FIRST_DAY(=25) >= MIN_1ST_DAY_AS_NEXT_MONTH(=16)
    2019/03 : 2019/02/25 ~ 2019/03/24
・FIRST_DAY(=5) < MIN_1ST_DAY_AS_NEXT_MONTH(=16)
    2019/03 : 2019/03/05 ~ 2019/04/04
"""

def bool_1st_day_as_next_month():
    """
    会計開始日を翌月に計上するかどうかを返す。
    """
    if FIRST_DAY >= MIN_1ST_DAY_AS_NEXT_MONTH:
        return True
    return False

def get_first_and_last_date(year, month):
    """
    会計開始日と終了日のdateオブジェクトを格納したディクショナリを返す。

    Parameters
    ----------
    year : int
        会計年。
    month : int
        会計月。
    """
    first_date = datetime.date(year=year, month=month, day=FIRST_DAY)
    if bool_1st_day_as_next_month():
        first_date -= relativedelta(months=1)

    last_date = first_date + relativedelta(months=1) - datetime.timedelta(days=1)

    return {'first_date': first_date, 'last_date': last_date}

def get_pay_and_period_date(year, month, pay_day, period_day=None):
    """
    支払日と締切日のdateオブジェクトを格納したディクショナリを返す。

    Parameters
    ----------
    year : int
        会計年。
    month : int
        会計月。
    pay_day : int
        支払日。
    period_day : int
        締切日。
    """
    pay_date = datetime.date(year=year, month=month, day=pay_day)
    if bool_1st_day_as_next_month():
        if pay_day >= FIRST_DAY:
            """
            例)
            ・2019/03: 2019/02/25 ~ 2019/03/24
                27日の支払 -> 2019/03/27 -> 2019/02/27
            """
            pay_date -= relativedelta(months=1)
    else:
        if pay_day < FIRST_DAY:
            """
            例)
            ・2019/03: 2019/03/5 ~ 2019/04/04
                3日の支払 -> 2019/03/03 -> 2019/04/03
            """
            pay_date += relativedelta(months=1)

    if period_day is None:
        period_date = None
    else:
        period_date = datetime.date(year=year, month=month, day=period_day)
        if bool_1st_day_as_next_month():
            if period_day >= FIRST_DAY:
                period_date -= relativedelta(months=1)
        else:
            if period_day < FIRST_DAY:
                period_date += relativedelta(months=1)

    return {'pay_date': pay_date, 'period_date': period_date}

# Create your views here.

def index(request):
    current_time = timezone.now()
    current_year = current_time.year
    current_month = current_time.month
    current_day = current_time.day
    if bool_1st_day_as_next_month():
        if current_day >= FIRST_DAY:
            # 翌月扱い
            current_month += 1
    else:
        if current_day < FIRST_DAY:
            # 先月扱い
            current_month -= 1

    # tableビューへリダイレクト
    return HttpResponseRedirect(
        reverse('income_and_expense:table', args=(current_year, current_month))
    )

def table(request, year, month):
    # バリデーション定義
    schema = {
        'year': {
            'type': 'integer',
            'min': MIN_YEAR,
            'max': MAX_YEAR,
        },
        'month': {
            'type': 'integer',
            'min': MIN_MONTH,
            'max': MAX_MONTH,           
        }
    }
    validator = Validator(schema)

    args = {
        'year': year,
        'month': month,
    }

    # バリデーション
    if not validator.validate(args):
        return HttpResponse("You are in invalid page.")

    # 会計開始日と終了日を取得
    first_and_last_day = get_first_and_last_date(year, month)
    first_date = first_and_last_day['first_date'] # 会計開始日
    last_date = first_and_last_day['last_date'] # 会計終了日

    # デフォルトの収入を追加    
    def_inc_months = DefaultIncomeMonth.objects.filter(month=month)
    this_month_incs = Income.objects.filter(pay_date__gte=first_date, pay_date__lte=last_date)
    for def_inc_month in def_inc_months:
        can_add = True
        def_inc = def_inc_month.def_inc # 追加対象の収入
        # 既に登録されているかのチェック
        for this_month_inc in this_month_incs:
            if def_inc.name == this_month_inc.name:
                # 既に登録されている場合
                can_add = False
                break
        # 追加
        if can_add:
            # まだ登録されていない場合
            pay_and_period_date = get_pay_and_period_date(
                year,
                month,
                def_inc.pay_day
            )
            inc = Income(
                name=def_inc.name,
                pay_date=pay_and_period_date['pay_date'],
                method=def_inc.method,
                amount=def_inc.amount,
                undecided=def_inc.undecided,
            )
            inc.save()

    # デフォルトの支出を追加
    def_exp_months = DefaultExpenseMonth.objects.filter(month=month)
    this_month_exps = Expense.objects.filter(period_date__gte=first_date, period_date__lte=last_date)
    for def_exp_month in def_exp_months:
        can_add = True
        def_exp = def_exp_month.def_exp # 追加対象の支出
        # 既に登録されているかのチェック
        for this_month_exp in this_month_exps:
            if def_exp.name == this_month_exp.name:
                # 既に登録されている場合
                can_add = False
                break
        # 追加
        if can_add:
            # まだ登録されていない場合
            pay_and_period_date = get_pay_and_period_date(
                year,
                month,
                def_exp.pay_day,
                def_exp.period_day
            )
            exp = Expense(
                name=def_exp.name,
                pay_date=pay_and_period_date['pay_date'],
                period_date=pay_and_period_date['period_date'],
                method=def_exp.method,
                amount=def_exp.amount,
                undecided=def_exp.undecided,
            )
            exp.save()

    # 先月、来月の年月を取得
    current_month_date = datetime.date(year=year, month=month, day=1) # 今月の代表日
    last_month_date = current_month_date - relativedelta(months=1) # 先月の代表日
    next_month_date = current_month_date + relativedelta(months=1) # 来月の代表日

    last_year = last_month_date.year # 先月の年
    last_mon = last_month_date.month # 先月の月
    next_year = next_month_date.year # 来月の年
    next_mon = next_month_date.month # 来月の月
    
    # 先月の口座残高を取得
    last_mon_balance = Settlement.objects.get(year=last_year, month=last_mon).balance

    # 今月の収支リストを取得
    this_month_incs = Income.objects.filter(pay_date__gte=first_date, pay_date__lte=last_date)
    this_month_exps = Expense.objects.filter(pay_date__gte=first_date, pay_date__lte=last_date)

    # 今月の収入の合計、支出の合計、残高を取得
    inc_sum = last_mon_balance + this_month_incs.aggregate(Sum('amount'))['amount__sum']
    exp_sum = this_month_exps.aggregate(Sum('amount'))['amount__sum']
    balance = inc_sum - exp_sum

    # 各口座の必要金額、実残高を取得
    accounts = Account.objects.all() # 全口座
    account_requires = [] # 各口座の必要金額
    account_balances = [] # 各口座の実残高
    account_balance_sum = 0 # 口座の実残高の合計

    for account in accounts:
        require = this_month_exps.filter(method__account=account, done=False).aggregate(Sum('amount'))['amount__sum']
        if require is None:
            require = 0
        account_require = {'account': account, 'require': "¥{:,}".format(require)}
        account_requires.append(account_require)
        account_balances.append({'account': account, 'balance': "¥{:,}".format(account.balance)})
        account_balance_sum += account.balance

    # DB上の残高を取得
    balance_on_db = last_mon_balance
    this_month_done_inc_sum = this_month_incs.filter(done=True).aggregate(Sum('amount'))['amount__sum']
    this_month_done_exp_sum = this_month_exps.filter(done=True).aggregate(Sum('amount'))['amount__sum']
    if this_month_done_inc_sum is not None:
        balance_on_db += this_month_done_inc_sum
    if this_month_done_exp_sum is not None:
        balance_on_db -= this_month_done_exp_sum

    # 口座の実残高とDB上残高の誤差を取得
    balance_diff = account_balance_sum - balance_on_db

    formset = IncomeFormSet()

    return render(request, 'income_and_expense/index.html', {
        'first_date': first_date,
        'last_date': last_date,
        'last_year': last_year,
        'last_mon': last_mon,
        'next_year': next_year,
        'next_mon': next_mon,
        'last_mon_balance': "¥{:,}".format(last_mon_balance),
        'incs': this_month_incs,
        'exps': this_month_exps,
        'inc_sum': "¥{:,}".format(inc_sum),
        'exp_sum': "¥{:,}".format(exp_sum),  
        'balance': "¥{:,}".format(balance),
        'account_requires': account_requires,
        'account_balances': account_balances,
        'account_balance_sum': "¥{:,}".format(account_balance_sum),
        'balance_on_db': "¥{:,}".format(balance_on_db),
        'balance_diff': "¥{:,}".format(balance_diff),
    })

    return HttpResponse("You are in page of {0}/{1}.".format(year, month))