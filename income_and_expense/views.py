import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from bootstrap_modal_forms.generic import (
    BSModalCreateView, BSModalUpdateView, BSModalDeleteView
)
from .models import (
    Expense, Income, DefaultExpenseMonth, DefaultIncomeMonth, Account,
    Method, TemplateExpense, Loan
)
from .forms import LoginForm, IncomeForm, ExpenseForm, BalanceForm, LoanForm
from .const import const_data

def can_add_default_inex(year, month):
    """デフォルトの収支を追加可能か判定する。

    Parameters
    ----------
    year : int
        会計年
    month : int
        会計月

    Returns
    -------
    bool
        デフォルト収支を追加可能かどうか
    """

    # 今月の初日を取得
    current_time = timezone.now()
    current_month_first_date = datetime.date(
        current_time.year, current_time.month, 1
    )

    # 過去には追加不可
    if datetime.date(year, month, 1) < current_month_first_date:
        return False

    return True

def can_update_or_delete_inex(year, month):
    """収支を更新・削除可能か判定する。

    Parameters
    ----------
    year : int
        現在の支払年
    month : int
        現在の支払月

    Returns
    -------
    bool
        収支を更新・削除可能かどうか
    """

    # 前月の初日を取得
    current_time = timezone.now()
    current_month_first_date = datetime.date(
        current_time.year, current_time.month, 1
    )
    last_month_first_date = (current_month_first_date
                             - relativedelta(months=1))

    # 現在の支払月の初日を取得
    old_pay_date = datetime.date(year, month, 1)

    # 現在の支払月が先月より前であった場合、更新を許可しない
    if old_pay_date < last_month_first_date:
        return False

    return True

def add_incs_from_default(year, month):
    """デフォルトの収支から収入を追加する。

    Parameters
    ----------
    year : int
        会計年
    month : int
        会計月

    Returns
    -------
    int
        追加した収入の数
    """

    # 会計開始日と終了日を取得
    first_date = datetime.date(year, month, 1)
    last_date = (
        first_date + relativedelta(months=1) - datetime.timedelta(days=1)
    )

    add_num = 0

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
            Income(
                name=def_inc.name,
                pay_date=datetime.date(year, month, def_inc.pay_day),
                method=def_inc.method, amount=def_inc.amount,
                undecided=def_inc.undecided,
            ).save()
            add_num += 1

    return add_num

def add_exps_from_default_and_loan(year, month):
    """デフォルトの支出とローンから支出を追加する。

    Parameters
    ----------
    year : int
        会計年
    month : int
        会計月

    Returns
    -------
    int
        追加した支出の数
    """

    # 会計開始日と終了日を取得
    first_date = datetime.date(year, month, 1)
    last_date = (
        first_date + relativedelta(months=1) - datetime.timedelta(days=1)
    )

    add_num = 0

    # デフォルトの支出から支出を追加
    def_exp_months = DefaultExpenseMonth.objects.filter(month=month)
    this_month_exps = Expense.objects.filter(
        pay_date__gte=first_date, pay_date__lte=last_date
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
            Expense(
                name=def_exp.name,
                pay_date=datetime.date(year, month, def_exp.pay_day),
                method=def_exp.method,
                amount=def_exp.amount, undecided=def_exp.undecided,
            ).save()
            add_num += 1

    # ローンから支出を追加
    loans = Loan.objects.filter(
        (Q(first_year__lt=year) | Q(first_year=year, first_month__lte=month)),
        (Q(last_year__gt=year) | Q(last_year=year, last_month__gte=month))
    )
    for loan in loans:
        can_add = True
        # 既に登録されているかのチェック
        for this_month_exp in this_month_exps:
            if loan.name == this_month_exp.name:
                # 既に登録されている場合
                can_add = False
                break
        # 追加
        if can_add:
            # まだ登録されていない場合
            if year == loan.first_year and month == loan.first_month:
                amount = loan.amount_first
            else:
                amount = loan.amount_from_second

            Expense(
                name=loan.name,
                pay_date=datetime.date(year, month, loan.pay_day),
                method=loan.method, amount=amount, undecided=loan.undecided,
            ).save()
            add_num += 1

    return add_num

def get_balance_done(year, month):
    """該当月までの残高（完了分）を取得

    Parameters
    ----------
    year : int
        会計年
    month : int
        会計月

    Returns
    -------
    int
        該当月までの残高（完了分）
    """

    # 会計開始日と終了日を取得
    first_date = datetime.date(year, month, 1)
    last_date = (
        first_date + relativedelta(months=1) - datetime.timedelta(days=1)
    )

    # 今月までの収支リストを取得
    incs_to_this_month = Income.objects.filter(
        pay_date__lte=last_date
    )
    exps_to_this_month = Expense.objects.filter(
        pay_date__lte=last_date
    )

    # 残高を計算
    # 今月までの収入（完了分）の合計
    done_incs = incs_to_this_month.filter(done=True)
    done_inc_sums = done_incs.aggregate(Sum('amount'))
    done_inc_sum = done_inc_sums['amount__sum']
    if done_inc_sum is None:
        done_inc_sum = 0
    # 今月の支出（完了分）を減算
    done_exps = exps_to_this_month.filter(done=True)
    done_exp_sums = done_exps.aggregate(Sum('amount'))
    done_exp_sum = done_exp_sums['amount__sum']
    if done_exp_sum is None:
        done_exp_sum = 0

    return done_inc_sum - done_exp_sum

def get_balance(year, month):
    """該当月までの残高を取得

    Parameters
    ----------
    year : int
        会計年
    month : int
        会計月

    Returns
    -------
    int
        該当月までの残高
    """

    # 会計開始日と終了日を取得
    first_date = datetime.date(year, month, 1)
    last_date = (
        first_date + relativedelta(months=1) - datetime.timedelta(days=1)
    )

    # 今月までの収支リストを取得
    incs_to_this_month = Income.objects.filter(
        pay_date__lte=last_date
    )
    exps_to_this_month = Expense.objects.filter(
        pay_date__lte=last_date
    )

    # 残高を計算
    # 今月までの収入（完了分）の合計
    inc_sums = incs_to_this_month.aggregate(Sum('amount'))
    inc_sum = inc_sums['amount__sum']
    if inc_sum is None:
        inc_sum = 0
    # 今月の支出（完了分）を減算
    exp_sums = exps_to_this_month.aggregate(Sum('amount'))
    exp_sum = exp_sums['amount__sum']
    if exp_sum is None:
        exp_sum = 0

    return inc_sum - exp_sum


# Create your views here.

class login(LoginView):
    form_class = LoginForm
    template_name = "income_and_expense/login.html"


class logout(LogoutView):
    pass


class IncomeCreateView(BSModalCreateView):
    template_name = 'income_and_expense/create_inc.html'
    form_class = IncomeForm
    success_message = '成功: %(name)sが追加されました。'

    def get_success_url(self):
        return reverse_lazy(
            'income_and_expense:income',
            args=[self.kwargs['year'], self.kwargs['month']]
        )


class IncomeUpdateView(BSModalUpdateView):
    model = Income
    template_name = 'income_and_expense/update_inc.html'
    form_class = IncomeForm
    success_message = '成功: %(name)sが更新されました。'

    def post(self, request, *args, **kwargs):
        if not can_update_or_delete_inex(kwargs['year'], kwargs['month']):
            messages.error(
                self.request,
                "失敗: 古い収入は更新できません。"
            )
            # incomeビューへリダイレクト
            return HttpResponseRedirect(
                reverse(
                    'income_and_expense:income',
                    args=(kwargs['year'], kwargs['month'])
                )
            )

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'income_and_expense:income',
            args=[self.kwargs['year'], self.kwargs['month']]
        )


class IncomeDeleteView(BSModalDeleteView):
    model = Income
    template_name = 'income_and_expense/delete_inc.html'
    form_class = IncomeForm

    def post(self, request, *args, **kwargs):
        pay_date = Income.objects.get(pk=kwargs['pk']).pay_date

        if not can_update_or_delete_inex(pay_date.year, pay_date.month):
            messages.error(
                self.request,
                "失敗: 古い収入は削除できません。"
            )
            # incomeビューへリダイレクト
            return HttpResponseRedirect(
                reverse(
                    'income_and_expense:income',
                    args=(kwargs['year'], kwargs['month'])
                )
            )

        messages.success(
            self.request,
            "成功: %sが削除されました。" % Income.objects.get(id=kwargs['pk']).name
        )
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'income_and_expense:income',
            args=[self.kwargs['year'], self.kwargs['month']]
        )


class ExpenseCreateView(BSModalCreateView):
    template_name = 'income_and_expense/create_exp.html'
    form_class = ExpenseForm
    success_message = '成功: %(name)sが追加されました。'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.date.today()
        template_exps = TemplateExpense.objects.all()
        context_template_exps = []

        for template_exp in template_exps:
            context_template_exp = {}

            # 名前（テンプレート）
            context_template_exp["template_name"] = str(template_exp.template_name)
            # 名前
            context_template_exp["name"] = str(template_exp.name)
            # 支払方法
            context_template_exp["method"] = str(template_exp.method)
            # 未定
            context_template_exp["undecided"] = str(template_exp.undecided)
            # 完了
            context_template_exp["done"] = str(template_exp.done)

            # 支払日
            if template_exp.date_type == 'today':
                pay_date = today
            else:
                if today.day <= template_exp.limit_day_of_this_month:
                    pay_date = datetime.date(
                        today.year, today.month, template_exp.pay_day
                    )
                else:
                    pay_date = datetime.date(
                        today.year, today.month, template_exp.pay_day
                    ) + relativedelta(months=1)
            context_template_exp["pay_date"] = "{0}-{1}-{2}".format(
                pay_date.year,
                str(pay_date.month).zfill(2),
                str(pay_date.day).zfill(2)
            )

            context_template_exps.append(context_template_exp)

        context['template_exps'] = context_template_exps
        return context

    def get_success_url(self):
        return reverse_lazy(
            'income_and_expense:expense',
            args=[self.kwargs['year'], self.kwargs['month']]
        )


class ExpenseUpdateView(BSModalUpdateView):
    model = Expense
    template_name = 'income_and_expense/update_exp.html'
    form_class = ExpenseForm
    success_message = '成功: %(name)sが更新されました。'

    def post(self, request, *args, **kwargs):
        if not can_update_or_delete_inex(kwargs['year'], kwargs['month']):
            messages.error(
                self.request,
                "失敗: 古い支出は更新できません。"
            )
            # incomeビューへリダイレクト
            return HttpResponseRedirect(
                reverse(
                    'income_and_expense:expense',
                    args=(kwargs['year'], kwargs['month'])
                )
            )

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'income_and_expense:expense',
            args=[self.kwargs['year'], self.kwargs['month']]
        )


class ExpenseDeleteView(BSModalDeleteView):
    model = Expense
    template_name = 'income_and_expense/delete_exp.html'
    form_class = ExpenseForm

    def post(self, request, *args, **kwargs):
        pay_date = Expense.objects.get(pk=kwargs['pk']).pay_date

        if not can_update_or_delete_inex(pay_date.year, pay_date.month):
            messages.error(
                self.request,
                "失敗: 古い支出は削除できません。"
            )
            # expenseビューへリダイレクト
            return HttpResponseRedirect(
                reverse(
                    'income_and_expense:expense',
                    args=(kwargs['year'], kwargs['month'])
                )
            )

        messages.success(
            self.request,
            "成功: %sが削除されました。" % Expense.objects.get(id=kwargs['pk']).name
        )
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'income_and_expense:expense',
            args=[self.kwargs['year'], self.kwargs['month']]
        )


class BalanceUpdateView(BSModalUpdateView):
    model = Account
    template_name = 'income_and_expense/update_balance.html'
    form_class = BalanceForm
    success_message = '成功: %(user)s%(bank)sが更新されました。'

    def get_success_url(self):
        return reverse_lazy(
            'income_and_expense:balance',
            args=[self.kwargs['year'], self.kwargs['month']]
        )


class LoanCreateView(BSModalCreateView):
    template_name = 'income_and_expense/create_loan.html'
    form_class = LoanForm
    success_message = '成功: %(name)sが追加されました。'

    def get_success_url(self):
        return reverse_lazy(
            'income_and_expense:loan',
            args=[self.kwargs['year'], self.kwargs['month']]
        )


class LoanUpdateView(BSModalUpdateView):
    model = Loan
    template_name = 'income_and_expense/update_loan.html'
    form_class = LoanForm
    success_message = '成功: %(name)sが更新されました。'

    def get_success_url(self):
        return reverse_lazy(
            'income_and_expense:loan',
            args=[self.kwargs['year'], self.kwargs['month']]
        )


class LoanDeleteView(BSModalDeleteView):
    model = Loan
    template_name = 'income_and_expense/delete_loan.html'
    form_class = LoanForm

    def post(self, request, *args, **kwargs):
        messages.success(
            self.request,
            "成功: %sが削除されました。" % Loan.objects.get(id=kwargs['pk']).name
        )
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'income_and_expense:loan',
            args=[self.kwargs['year'], self.kwargs['month']]
        )


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

    # incomeビューへリダイレクト
    return HttpResponseRedirect(
        reverse(
            'income_and_expense:income',
            args=(current_time.year, current_time.month)
        )
    )

@login_required
def move_another_page(request):
    """別画面移動用のビュー関数。

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト

    Returns
    -------
    HttpResponseRedirect
        HttpResponseRedirectオブジェクト
    """

    # 適切なビューへリダイレクト
    return HttpResponseRedirect(
        reverse(
            request.GET.get("path_name"),
            args=(request.GET.get("year"), request.GET.get("month"))
        )
    )

@login_required
def income(request, year, month):
    """income用のビュー関数。

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

    # 会計開始日と終了日を取得
    first_date = datetime.date(year, month, 1)
    last_date = (
        first_date + relativedelta(months=1) - datetime.timedelta(days=1)
    )

    # 先月の代表日
    last_month_date = first_date - relativedelta(months=1)

    # 先月までの口座残高を取得
    last_mon_balance = get_balance(
        last_month_date.year, last_month_date.month
    )

    # 今月の収入リストを取得
    this_month_incs = Income.objects.order_by(
        'method__account__user', 'method'
    ).filter(pay_date__gte=first_date, pay_date__lte=last_date)

    # 今月の収入の合計を取得
    inc_sum = (last_mon_balance
               + (this_month_incs.aggregate(Sum('amount'))['amount__sum'] or 0))

    return render(request, 'income_and_expense/income.html', {
        'path_name': const_data.const.PATH_NAME_INCOME,
        'this_year': year,
        'this_mon': month,
        'incs': this_month_incs,
        'last_mon_balance': last_mon_balance,
        'inc_sum': inc_sum,
    })

@login_required
def add_default_incs(request, year, month):
    """add_default_incs用のビュー関数。

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

    # デフォルトの収入から収入を追加
    if can_add_default_inex(year, month):
        if add_incs_from_default(year, month) > 0:
            messages.success(request, "成功: デフォルト収入が追加されました。")
        else:
            messages.error(request, "失敗: 追加できるデフォルト収入が存在しませんでした。")
    else:
        messages.error(request, "失敗: 過去にはデフォルト収入を追加できません。")

    # incomeビューへリダイレクト
    return HttpResponseRedirect(
        reverse(
            'income_and_expense:income',
            args=(year, month)
        )
    )

@login_required
def expense(request, year, month):
    """expense用のビュー関数。

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

    # 会計開始日と終了日を取得
    first_date = datetime.date(year, month, 1)
    last_date = (
        first_date + relativedelta(months=1) - datetime.timedelta(days=1)
    )

    # 先月の代表日
    last_month_date = first_date - relativedelta(months=1)

    # 先月の口座残高を取得
    last_mon_balance = get_balance(
        last_month_date.year, last_month_date.month
    )

    # 今月の支出リストを取得
    this_month_exps = Expense.objects.order_by(
        'method__account__user', 'method'
    ).filter(pay_date__gte=first_date, pay_date__lte=last_date)

    # 今月の支出の合計を取得
    exp_sum = this_month_exps.aggregate(Sum('amount'))['amount__sum'] or 0

    # 今月の残高を取得
    balance = get_balance(year, month)

    return render(request, 'income_and_expense/expense.html', {
        'path_name': const_data.const.PATH_NAME_EXPENSE,
        'this_year': year,
        'this_mon': month,
        'exps': this_month_exps,
        'exp_sum': exp_sum,
        'balance': balance,
    })

@login_required
def add_default_exps(request, year, month):
    """add_default_exps用のビュー関数。

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

    # デフォルトの支出とローンから支出を追加
    if can_add_default_inex(year, month):
        if add_exps_from_default_and_loan(year, month) > 0:
            messages.success(request, "成功: デフォルト支出が追加されました。")
        else:
            messages.error(request, "失敗: 追加できるデフォルト支出が存在しませんでした。")
    else:
        messages.error(request, "失敗: 過去にはデフォルト支出を追加できません。")

    # expsenseビューへリダイレクト
    return HttpResponseRedirect(
        reverse(
            'income_and_expense:expense',
            args=(year, month)
        )
    )

@login_required
def balance(request, year, month):
    """balanceページ用のビュー関数。

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

    # 各口座の実残高を取得
    accounts = Account.objects.all().order_by('user') # 全口座
    balances = [] # 各口座の実残高
    balance_sum = 0 # 口座の実残高の合計
    for account in accounts:
        balances.append({
            'account': account, 'balance': "¥{:,}".format(account.balance)
        })
        balance_sum += account.balance

    # DB上の残高（完了分）を取得
    balance_on_db = get_balance_done(year, month)

    # 口座の実残高とDB上残高（完了分）の誤差を取得
    balance_diff = balance_sum - balance_on_db

    return render(request, 'income_and_expense/balance.html', {
        'path_name': const_data.const.PATH_NAME_BALANCE,
        'this_year': year,
        'this_mon': month,
        'accounts': accounts,
        'balance_sum': balance_sum,
        'balance_on_db': balance_on_db,
        'balance_diff': balance_diff,
    })

@login_required
def account_require(request, year, month):
    """account_requireページ用のビュー関数。

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

    # 会計開始日と終了日を取得
    first_date = datetime.date(year, month, 1)
    last_date = (
        first_date + relativedelta(months=1) - datetime.timedelta(days=1)
    )

    # 今月の支出リストを取得
    this_month_exps = Expense.objects.filter(
        pay_date__gte=first_date, pay_date__lte=last_date
    )

    # 各口座の必要金額を取得
    accounts = Account.objects.all().order_by('user') # 全口座
    account_requires = [] # 各口座の必要金額
    require_sum = 0 # 必要金額の合計値
    insufficient_sum = 0 # 不足額の合計値
    is_insufficient = False # 口座残高が不足しているかどうか
    insufficient_amount = 0 # 各口座の不足額
    for account in accounts:
        require = this_month_exps.filter(
            method__account=account, done=False
        ).aggregate(Sum('amount'))['amount__sum']
        if require is None:
            require = 0

        require_sum += require

        if account.balance < require:
            is_insufficient = True
            insufficient_amount = require - account.balance
        else:
            is_insufficient = False
            insufficient_amount = 0

        insufficient_sum += insufficient_amount

        account_require = {
            'account': account, 'require': "¥{:,}".format(require),
            'is_insufficient': is_insufficient,
            'insufficient_amount': "¥{:,}".format(insufficient_amount)
        }
        account_requires.append(account_require)

    return render(request, 'income_and_expense/account_require.html', {
        'path_name': const_data.const.PATH_NAME_ACCOUNT_REQUIRE,
        'this_year': year,
        'this_mon': month,
        'account_requires': account_requires,
        'require_sum': "¥{:,}".format(require_sum),
        'insufficient_sum': "¥{:,}".format(insufficient_sum),
    })

@login_required
def method_require(request, year, month):
    """method_requireページ用のビュー関数。

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

    # 会計開始日と終了日を取得
    first_date = datetime.date(year, month, 1)
    last_date = (
        first_date + relativedelta(months=1) - datetime.timedelta(days=1)
    )

    # 今月の支出リストを取得
    this_month_exps = Expense.objects.filter(
        pay_date__gte=first_date, pay_date__lte=last_date
    )

    # 支払方法別の必要金額を取得
    # 全支払方法
    methods = Method.objects.all().order_by(
        'account__user', 'account__bank'
    )
    method_requires = [] # 支払方法別の必要金額
    require_sum = 0 # 必要金額の合計値
    for method in methods:
        require = this_month_exps.filter(
            method=method, done=False
        ).aggregate(Sum('amount'))['amount__sum']
        if require is None:
            require = 0

        require_sum += require

        method_require = {
            'method': method, 'require': "¥{:,}".format(require),
        }
        method_requires.append(method_require)

    return render(request, 'income_and_expense/method_require.html', {
        'path_name': const_data.const.PATH_NAME_METHOD_REQUIRE,
        'this_year': year,
        'this_mon': month,
        'method_requires': method_requires,
        'require_sum': "¥{:,}".format(require_sum),
    })


@login_required
def method_done(request, year, month, pk):
    """method_doneページ用のビュー関数。

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト
    year : int
        会計年
    month : int
        会計月
    pk : int
        支払方法のpk

    Returns
    -------
    HttpResponse
        HttpResponseオブジェクト
    """

    # 会計開始日と終了日を取得
    first_date = datetime.date(year, month, 1)
    last_date = (
            first_date + relativedelta(months=1) - datetime.timedelta(days=1)
    )

    # 該当の支払方法の支出をすべて支払済に変更
    target_exps = Expense.objects.filter(method__pk=pk,
        pay_date__gte=first_date, pay_date__lte=last_date
    )
    for target_exp in target_exps:
        target_exp.done = True
        target_exp.undecided = False
        target_exp.save()

    messages.success(request, "成功: 支払済一括登録されました。")

    # method_requireビューへリダイレクト
    return HttpResponseRedirect(
        reverse(
            'income_and_expense:method_require',
            args=(year, month)
        )
    )

@login_required
def loan(request, year, month):
    """loanページ用のビュー関数。

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

    loans_and_completes = [] # 各ローンと終了しているかどうか

    # ローン一覧を取得
    loans = Loan.objects.all().order_by('method') # 全ローン

    for loan in loans:
        loan_and_complete = {}
        loan_and_complete['loan'] = loan

        is_over_year = year > loan.last_year
        is_same_year_and_over_month = (
            (year == loan.last_year) and (month > loan.last_month)
        )
        loan_and_complete['complete'] = (
            is_over_year or is_same_year_and_over_month
        )

        loans_and_completes.append(loan_and_complete)

    return render(request, 'income_and_expense/loan.html', {
        'path_name': const_data.const.PATH_NAME_LOAN,
        'this_year': year,
        'this_mon': month,
        'loans_and_completes': loans_and_completes,
    })