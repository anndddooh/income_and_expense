import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from cerberus import Validator
from dateutil.relativedelta import relativedelta

from .models import (
    Expense, Income, DefaultExpenseMonth, DefaultIncomeMonth,
    Settlement, Account
)
from .forms import IncomeFormSet, ExpenseFormSet, AccountBalanceFormSet

MIN_YEAR = 2019
MAX_YEAR = 2025
MIN_MONTH = 1
MAX_MONTH = 12
FIRST_DAY = 28 # 各月の会計開始日
MIN_1ST_DAY_AS_NEXT_MONTH = 16 # 翌月扱いする会計開始日の最小値

def bool_1st_day_as_next_month():
    """会計開始日を翌月に計上するかどうかを返す。

    Returns
    -------
    bool
        会計開始日を翌月に計上するかどうか
    """
    if FIRST_DAY >= MIN_1ST_DAY_AS_NEXT_MONTH:
        return True
    return False

def get_first_and_last_date(year, month):
    """会計開始日と終了日のdateオブジェクトを格納した
        ディクショナリを返す。
    
    Parameters
    ----------
    year : int
        会計年
    month : int
        会計月
    
    Returns
    -------
    dict
        会計開始日と終了日のdateオブジェクトを格納したディクショナリ
    """
    first_date = datetime.date(year=year, month=month, day=FIRST_DAY)
    if bool_1st_day_as_next_month():
        first_date -= relativedelta(months=1)

    last_date = (first_date + relativedelta(months=1)
                - datetime.timedelta(days=1))

    return {'first_date': first_date, 'last_date': last_date}

def get_pay_and_period_date(year, month, pay_day, period_day=None):
    """支払日と締切日のdateオブジェクトを格納したディクショナリを返す。
    
    Parameters
    ----------
    year : int
        会計年
    month : int
        会計月
    pay_day : int
        支払日
    period_day : int or None, default None
        締切日
    
    Returns
    -------
    dict
        支払日と締切日のdateオブジェクトを格納したディクショナリ
    """
    pay_date = datetime.date(year=year, month=month, day=pay_day)
    if bool_1st_day_as_next_month():
        if pay_day >= FIRST_DAY:
            """
            Example
            ・2019/03: 2019/02/25 ~ 2019/03/24
                27日の支払 -> 2019/03/27 -> 2019/02/27
            """
            pay_date -= relativedelta(months=1)
    else:
        if pay_day < FIRST_DAY:
            """
            Example
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

def add_incs_from_default(year, month):
    """デフォルトの収支から収入を追加する。
    
    Parameters
    ----------
    year : int
        会計年
    month : int
        会計月
    """
    # 会計開始日と終了日を取得
    first_and_last_day = get_first_and_last_date(year, month)
    first_date = first_and_last_day['first_date'] # 会計開始日
    last_date = first_and_last_day['last_date'] # 会計終了日

    # デフォルトの収入から収入を追加    
    def_inc_months = DefaultIncomeMonth.objects.filter(month=month)
    this_month_incs = Income.objects.filter(
        pay_date__gte=first_date, pay_date__lte=last_date
    )
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
                year, month, def_inc.pay_day
            )
            inc = Income(
                name=def_inc.name, pay_date=pay_and_period_date['pay_date'],
                method=def_inc.method, amount=def_inc.amount,
                undecided=def_inc.undecided,
            )
            inc.save()

def add_exps_from_default(year, month):
    """デフォルトの支出から支出を追加する。
    
    Parameters
    ----------
    year : int
        会計年
    month : int
        会計月
    """
    # 会計開始日と終了日を取得
    first_and_last_day = get_first_and_last_date(year, month)
    first_date = first_and_last_day['first_date'] # 会計開始日
    last_date = first_and_last_day['last_date'] # 会計終了日

    # デフォルトの支出から支出を追加    
    def_exp_months = DefaultExpenseMonth.objects.filter(month=month)
    this_month_exps = Expense.objects.filter(
        period_date__gte=first_date, period_date__lte=last_date
    )
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
                year, month, def_exp.pay_day, def_exp.period_day
            )
            exp = Expense(
                name=def_exp.name, pay_date=pay_and_period_date['pay_date'],
                period_date=pay_and_period_date['period_date'],
                method=def_exp.method, amount=def_exp.amount,
                undecided=def_exp.undecided,
            )
            exp.save()

def validate_url_in_table_page(year, month):
    """テーブルページのURLのバリデーションをおこなう。
    
    Parameters
    ----------
    year : int
        会計年
    month : int
        会計月
    
    Returns
    -------
    bool
        バリデーション結果
    """
    # バリデーション定義
    schema = {
        'year': {
            'type': 'integer', 'min': MIN_YEAR, 'max': MAX_YEAR,
        },
        'month': {
            'type': 'integer', 'min': MIN_MONTH, 'max': MAX_MONTH,           
        }
    }

    validator = Validator(schema)

    args = {
        'year': year, 'month': month,
    }

    # バリデーション
    return validator.validate(args)


# Create your views here.

@login_required
def index(request):
    """トップページ用のビュー関数。
    
    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト
    
    Returns
    -------
    HttpResponseRedirect
        HttpResponseRedirectオブジェクト
    """
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
        reverse(
            'income_and_expense:table', args=(current_year, current_month)
        )
    )

@login_required
def table(request, year, month):
    """テーブルページ用のビュー関数。
    
    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト
    year : int
        会計年
    month : int
        会計月
    
    Returns
    -------
    HttpResponse
        HttpResponseオブジェクト
    """
    # バリデーション
    if not validate_url_in_table_page(year, month):
        return HttpResponse("You are in invalid page.")

    # 会計開始日と終了日を取得
    first_and_last_day = get_first_and_last_date(year, month)
    first_date = first_and_last_day['first_date'] # 会計開始日
    last_date = first_and_last_day['last_date'] # 会計終了日

    # デフォルトの収入から収入を追加
    this_month_inc_cnt = Income.objects.filter(
        pay_date__gte=first_date, pay_date__lte=last_date
    ).count()
    if this_month_inc_cnt == 0:
        # 収入が一件も登録されていない場合
        add_incs_from_default(year, month)
    
    # デフォルトの支出から支出を追加
    this_month_exp_cnt = Expense.objects.filter(
        pay_date__gte=first_date, pay_date__lte=last_date
    ).count()
    if this_month_exp_cnt == 0:
        # 支出が一件も登録されていない場合
        add_exps_from_default(year, month)

    # 先月、来月の年と月を取得
    # 今月の代表日
    current_month_date = datetime.date(year=year, month=month, day=1)
    # 先月の代表日
    last_month_date = current_month_date - relativedelta(months=1)
    # 来月の代表日
    next_month_date = current_month_date + relativedelta(months=1)
    last_year = last_month_date.year # 先月の年
    last_mon = last_month_date.month # 先月の月
    next_year = next_month_date.year # 来月の年
    next_mon = next_month_date.month # 来月の月
    
    # 先月の口座残高を取得
    last_mon_balance = Settlement.objects.get(
        year=last_year, month=last_mon
    ).balance

    # 今月の収支リストを取得
    this_month_incs = Income.objects.filter(
        pay_date__gte=first_date, pay_date__lte=last_date
    )
    this_month_exps = Expense.objects.filter(
        pay_date__gte=first_date, pay_date__lte=last_date
    )
    
    # 今月の収支リストのフォームを作成
    this_month_inc_forms = IncomeFormSet(queryset=this_month_incs)
    this_month_exp_forms = ExpenseFormSet(queryset=this_month_exps)

    # 今月の収入の合計、支出の合計、残高を取得
    inc_sum = (last_mon_balance
                + this_month_incs.aggregate(Sum('amount'))['amount__sum'])
    exp_sum = this_month_exps.aggregate(Sum('amount'))['amount__sum']
    balance = inc_sum - exp_sum

    # 今月の残高を更新
    this_mon_settlement = None
    if Settlement.objects.filter(year=year, month=month).exists():
        this_mon_settlement = Settlement.objects.get(year=year, month=month)
    else:
        this_mon_settlement = Settlement(year=year, month=month, balance=0)
    this_mon_settlement.balance = balance
    this_mon_settlement.save()

    # 各口座の必要金額、実残高を取得
    accounts = Account.objects.all() # 全口座
    account_requires = [] # 各口座の必要金額
    account_balances = [] # 各口座の実残高
    account_balance_sum = 0 # 口座の実残高の合計
    for account in accounts:
        require = this_month_exps.filter(
            method__account=account, done=False
        ).aggregate(Sum('amount'))['amount__sum']
        if require is None:
            require = 0
        account_require = {
            'account': account, 'require': "¥{:,}".format(require)
        }
        account_requires.append(account_require)
        account_balances.append({
            'account': account, 'balance': "¥{:,}".format(account.balance)
        })
        account_balance_sum += account.balance

    # 各口座の残高のフォームを作成
    account_balance_forms = AccountBalanceFormSet()

    # DB上の残高を取得
    balance_on_db = last_mon_balance
    done_incs = this_month_incs.filter(done=True)
    done_inc_sums = done_incs.aggregate(Sum('amount'))
    done_inc_sum = done_inc_sums['amount__sum']
    if done_inc_sum is not None:
        balance_on_db += done_inc_sum  
    done_exps = this_month_exps.filter(done=True)
    done_exp_sums = done_exps.aggregate(Sum('amount'))
    done_exp_sum = done_exp_sums['amount__sum']
    if done_exp_sum is not None:
        balance_on_db -= done_exp_sum

    # 口座の実残高とDB上残高の誤差を取得
    balance_diff = account_balance_sum - balance_on_db

    return render(request, 'income_and_expense/index.html', {
        'first_date': first_date,
        'last_date': last_date,
        'this_year': year,
        'this_mon': month,
        'last_year': last_year,
        'last_mon': last_mon,
        'next_year': next_year,
        'next_mon': next_mon,
        'last_mon_balance': last_mon_balance,
        'incs': this_month_incs,
        'exps': this_month_exps,
        'inc_forms': this_month_inc_forms,
        'exp_forms': this_month_exp_forms,
        'inc_sum': inc_sum,
        'exp_sum': exp_sum,  
        'balance': balance,
        'account_requires': account_requires,
        'account_balances': account_balances,
        'account_balance_forms': account_balance_forms,
        'account_balance_sum': account_balance_sum,
        'balance_on_db': balance_on_db,
        'balance_diff': balance_diff,
    })

@login_required
def modify_income(request, year, month):
    """modify_incページ用のビュー関数。
    
    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト
    year : int
        会計年
    month : int
        会計月
    
    Returns
    -------
    HttpResponseRedirect
        HttpResponseRedirectオブジェクト
    """
    # incomeを更新
    if request.method == 'POST':
        formset = IncomeFormSet(request.POST or None)
        if formset.is_valid():
            formset.save()

    # tableビューへリダイレクト
    return HttpResponseRedirect(
        reverse('income_and_expense:table', args=(year, month))
    )

@login_required
def modify_expense(request, year, month):
    """modify_expページ用のビュー関数。
    
    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト
    year : int
        会計年
    month : int
        会計月
    
    Returns
    -------
    HttpResponseRedirect
        HttpResponseRedirectオブジェクト
    """
    # expenseを更新
    if request.method == 'POST':
        formset = ExpenseFormSet(request.POST or None)
        if formset.is_valid():
            formset.save()

    # tableビューへリダイレクト
    return HttpResponseRedirect(
        reverse('income_and_expense:table', args=(year, month))
    )

@login_required
def modify_account_balance(request, year, month):
    """modify_balanceページ用のビュー関数。
    
    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト
    year : int
        会計年
    month : int
        会計月        
    
    Returns
    -------
    HttpResponseRedirect
        HttpResponseRedirectオブジェクト
    """
    # accountのbalanceを更新
    if request.method == 'POST':
        formset = AccountBalanceFormSet(request.POST or None)
        if formset.is_valid():
            formset.save()

    # tableビューへリダイレクト
    return HttpResponseRedirect(
        reverse('income_and_expense:table', args=(year, month))
    )