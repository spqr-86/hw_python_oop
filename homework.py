import datetime as dt


class Calculator:
    def __init__(self, limit: float):
        self.limit = limit
        self.records = []

    today = dt.date.today()

    def add_record(self, record):

        self.records.append(record)

    def get_today_stats(self):
        return sum(e.amount for e in self.records if e.date == self.today)

    def get_week_stats(self):
        return sum(e.amount for e in self.records if
                   (self.today + dt.timedelta(1)) > e.date >=
                   (self.today - dt.timedelta(7)))


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

    LEFT = 'Сегодня можно съесть что-нибудь ещё, ' \
           'но с общей калорийностью не более {} кКал'

    STOP = 'Хватит есть!'

    def get_calories_remained(self):

        today_stats = self.get_today_stats()

        calories_remained = self.limit - today_stats

        if calories_remained > 0:
            return self.LEFT.format(calories_remained)
        else:
            return self.STOP


class CashCalculator(Calculator):

    EURO_RATE = 70.0
    USD_RATE = 60.0

    d_currency = {
        'eur': ['Euro', EURO_RATE],
        'usd': ['USD', USD_RATE],
        'rub': ['руб', 1]}

    LEFT = 'На сегодня осталось {} {}'
    NO = 'Денег нет, держись'
    DEBT = 'Денег нет, держись: твой долг - {} {}'

    def get_today_cash_remained(self, currency):

        today_stats = self.get_today_stats()
        cash_remained = (self.limit - today_stats)/self.d_currency[currency][1]
        cur = self.d_currency[currency][0]

        if cash_remained > 0:
            return self.LEFT.format(round(cash_remained, 2), cur)
        elif cash_remained == 0:
            return self.NO
        else:
            return self.DEBT.format(round(abs(cash_remained), 2), cur)
