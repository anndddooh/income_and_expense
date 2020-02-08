from django.db import models
from django.core import validators

# Create your models here.


class Bank(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    balance = models.PositiveIntegerField()

    class Meta:
        # 他レコードで同じ'bank'と'user'の組み合わせを許さない
        unique_together = ('bank', 'user')

    def __str__(self):
        return "{0}{1}".format(self.user, self.bank)
    

class Method(models.Model):
    name = models.CharField(max_length=50)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)

    def __str__(self):
        my_str = self.name
        patterns = ['振込', '預入', '現金', '引き落とし']
        for pattern in patterns:
            if pattern in my_str:
                my_str = "{0}({1})".format(self.name, self.account)
        return my_str


class Expense(models.Model):
    name = models.CharField(max_length=50)
    pay_date = models.DateField('payment date')
    method = models.ForeignKey(Method, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    undecided = models.BooleanField()
    done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'pay_date')

    def __str__(self):
        return self.name

    def account_info(self):
        return self.method.account
    account_info.short_description = 'account'

    def formed_amount(self):
        return "¥{:,}".format(self.amount)
    formed_amount.short_description = 'amount'


class Income(models.Model):
    name = models.CharField(max_length=50)
    pay_date = models.DateField('payment date')
    method = models.ForeignKey(Method, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    undecided = models.BooleanField()
    done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'pay_date')

    def __str__(self):
        return self.name

    def account_info(self):
        return self.method.account
    account_info.short_description = 'account'

    def formed_amount(self):
        return "¥{:,}".format(self.amount)
    formed_amount.short_description = 'amount'


class DefaultExpense(models.Model):
    name = models.CharField(max_length=50, unique=True)
    pay_day = models.PositiveIntegerField(validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(28)
    ])
    period_day = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(28)
        ],
        null=True
    )
    method = models.ForeignKey(Method, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    undecided = models.BooleanField()

    def __str__(self):
        return self.name

    def account_info(self):
        return self.method.account
    account_info.short_description = 'account'

    def formed_amount(self):
        return "¥{:,}".format(self.amount)
    formed_amount.short_description = 'amount'


class DefaultIncome(models.Model):
    name = models.CharField(max_length=50, unique=True)
    pay_day = models.PositiveIntegerField(validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(28)
    ])
    method = models.ForeignKey(Method, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    undecided = models.BooleanField()

    def __str__(self):
        return self.name

    def account_info(self):
        return self.method.account
    account_info.short_description = 'account'

    def formed_amount(self):
        return "¥{:,}".format(self.amount)
    formed_amount.short_description = 'amount'


class DefaultExpenseMonth(models.Model):
    month = models.PositiveIntegerField(validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(12)
    ])
    def_exp = models.ForeignKey(DefaultExpense, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('month', 'def_exp')

    def __str__(self):
        return "{0}({1}月)".format(self.def_exp, self.month)

    def def_exp_name(self):
        return self.def_exp


class DefaultIncomeMonth(models.Model):
    month = models.PositiveIntegerField(validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(12)
    ])
    def_inc = models.ForeignKey(DefaultIncome, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('month', 'def_inc')

    def __str__(self):
        return "{0}({1}月)".format(self.def_inc, self.month)

    def def_inc_name(self):
        return self.def_inc