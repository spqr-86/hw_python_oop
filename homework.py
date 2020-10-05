import datetime as dt


class Calculator:
    def __init__(self, limit: float):
        self.limit = limit
        self.records = []

    def add_record(self, record):

        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for i in self.records:
            if i.date == dt.datetime.now().date():
                today_stats += i.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        for i in self.records:
            if (dt.datetime.now().date() + dt.timedelta(1)) \
                    > i.date >= (dt.datetime.now().date() - dt.timedelta(7)):
                week_stats += i.amount
        return week_stats


class Record:
    def __init__(self, amount, comment, date=str(dt.datetime.now().strftime('%d.%m.%Y'))):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        moment = dt.datetime.strptime(date, date_format)
        self.date = moment.date()


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):

        today_stats = self.get_today_stats()

        calories_remained = self.limit - today_stats

        if calories_remained > 0:
            return f'Сегодня можно съесть что-нибудь ещё, ' \
                f'но с общей калорийностью не более {calories_remained} кКал'
        else:
            return f'Хватит есть!'


class CashCalculator(Calculator):

    EURO_RATE = 91.92
    USD_RATE = 78.1

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):

        today_stats = self.get_today_stats()

        if currency == 'eur':
            cash_remained = (self.limit - today_stats)/self.EURO_RATE
            cur = 'Euro'
        elif currency == 'rub':
            cash_remained = self.limit - today_stats
            cur = 'руб'
        elif currency == 'usd':
            cash_remained = (self.limit - today_stats)/self.USD_RATE
            cur = 'USD'
        else:
            cash_remained = self.limit - today_stats
            cur = 'руб'

        if cash_remained > 0:
            return f'На сегодня осталось {round(cash_remained, 2)} {cur}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - ' \
                f'{round(abs(cash_remained), 2)} {cur}'

