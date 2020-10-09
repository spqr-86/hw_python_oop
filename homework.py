import datetime as dt


class Calculator:

    def __init__(self, limit: float):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(e.amount for e in self.records if e.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        weak = today - dt.timedelta(7)

        return sum(e.amount for e in self.records if weak < e.date <= today)


class Record:

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            moment = dt.datetime.strptime(date, self.DATE_FORMAT)
            self.date = moment.date()


class CaloriesCalculator(Calculator):

    LEFT = ('Сегодня можно съесть что-нибудь ещё, '
            'но с общей калорийностью не более {} кКал')
    STOP = 'Хватит есть!'

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        calories_remained = self.limit - today_stats
        if calories_remained > 0:
            return self.LEFT.format(calories_remained)
        return self.STOP


class CashCalculator(Calculator):

    EURO_RATE = 70.0
    USD_RATE = 60.0
    currency_items = {
        'eur': ['Euro', EURO_RATE],
        'usd': ['USD', USD_RATE],
        'rub': ['руб', 1]}
    LEFT = 'На сегодня осталось {cash} {currency}'
    NO = 'Денег нет, держись'
    DEBT = 'Денег нет, держись: твой долг - {cash} {currency}'

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()
        limit = self.limit - today_stats
        if limit == 0:
            return self.NO
        rate = self.currency_items[currency][1]
        signature = self.currency_items[currency][0]
        cash = round(limit/rate, 2)
        if limit > 0:
            return self.LEFT.format(cash=cash,
                                    currency=signature)
        return self.DEBT.format(cash=abs(cash),
                                currency=signature)
