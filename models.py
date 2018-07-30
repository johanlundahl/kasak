from datetime import datetime, timedelta

class Week:
    def __init__(self, of_year, number):
        self._of_year = of_year
        self._number = number
        
    @classmethod
    def from_date(self, date):
        return Week(date.year, date.isocalendar()[1])    
    
    @classmethod
    def from_day(self, day):
        return Week.from_date(day.datetime())

    def weekdays(self):
        weekdays = []
        day = Day.from_datetime(self.first_date())
        while day.is_weekday():
            weekdays.append(day)
            day = day.next()
        return weekdays
        
    def first_date(self):
        return datetime.strptime('{}-W{}-1'.format(self._of_year, self._number), '%Y-W%W-%w').date()

class Day:
    def __init__(self, day):
        self.day = day
    
    @staticmethod
    def from_datetime(datetime):
        return Day(datetime.strftime('%Y-%m-%d'))
    
    @staticmethod
    def today():
        return Day.from_datetime(datetime.now())
    
    def next(self):
        next = self.datetime() + timedelta(days=1)
        return Day(next.strftime('%Y-%m-%d'))
    
    def is_weekday(self):
        return self.datetime().weekday() < 5

    def date(self):
        return self.day    
    
    def datetime(self):
        return datetime.strptime(self.day, '%Y-%m-%d')

    def name(self):
        return self.datetime().strftime('%A')

    def short_name(self):
        return self.datetime().strftime('%a')
    
    def __eq__(self, other):
        return self.date() == other.date()
        
    def __le__(self, other):
        return self.datetime() <= other.datetime()
    
    def __str__(self):
        return self.day

class CarWash:
    def __init__(self, reg, date, pickup_time, return_time, company, picked_up=False, returned=False, comment='', pickup_assigned=None, return_assigned=None):
        self.reg = reg
        self.date = date
        self.pickup_time = pickup_time
        self.return_time = return_time
        self.pickup_assigned = pickup_assigned
        self.return_assigned = return_assigned
        self.company = company
        self.picked_up = int(picked_up)
        self.returned = int(returned)
        self.comment = comment

    def __str__(self):
        return '{} {} {} {} {}'.format(self.reg, self.date, self.picked_up, self.returned, self.comment)       

#Rename to reservation
class Booking:
    def __init__(self, customer, reg, week, weekday, pickup_time, count, interval, package, fluid, comment):
        self._customer = customer
        self._reg = reg
        self._week = week
        self._count = int(count) if count != '' else 0
        self._interval = int(interval) if interval != '' else 0
        self._weekday = int(weekday) if weekday != '' else 0
        self._time = pickup_time
        self._comment = comment

    @staticmethod
    def parse(kund, reg, vecka, antal, intervall, dag, tid, kommentar):
        return Booking(kund, reg, vecka, dag, tid, antal, intervall, 'Kommun', 1, kommentar)
    
    @property
    def customer(self):
        return self._customer

    @property
    def reg(self):
        return self._reg
    
    @property
    def week(self):
        return int(self._week) if self._week != '' else 0
    
    @property
    def date(self):
        days_offset = (int(self.week)-1)*7 + int(self._weekday)-1
        start_date = self.period_start_date.date() + timedelta(days=days_offset)
        return str(Day.from_datetime(start_date))
        
    def period_start(self, date):
        self.period_start_date = date

    @property
    def pickup_time(self):
        return self._time.strftime("%H:%M")
    
    @property
    def return_time(self):
        if self._time == '':
            return ''
        return '12:00' if self._time.hour < 12 else '16:00'
    
    @property
    def recurrent(self):
        return 'on' if self.interval > 0 and self.count > 0 else 'off'
        
    @property
    def count(self):
        return self._count
    
    @property
    def interval(self):
        return self._interval
    
    @property
    def package(self):
        return 'Kommun'
    
    @property
    def liquid(self):
        return '1'
    
    @property
    def comment(self):
        return self._comment
    
    def __repr__(self):
        return 'Booking(reg={}, kund={}, datum={})'.format(self.reg, self.customer, self.date)
        
    def __str__(self):
        return '{};{};{};{};{};{};{};{};{};{}'.format(self.reg, self.date, self.pickup_time, self.return_time, 
                                                    self.recurrent, self.count, self.interval,
                                                    self.package, self.liquid, self.comment)

class Customer:
    def __init__(self, customer, address, postal_code, city, first_name=None, last_name=None, phone=None, email=None):
        self._first_name = first_name
        self._last_name = last_name
        self._customer = customer
        self._phone = phone
        self._email = email
        self._address = address
        self._postal_code = postal_code
        self._city = city
    
    @staticmethod
    def parse(typ, kund, adress, postnummer, postort, **args):
        return Customer(kund, adress, postnummer, postort)
    
    @property
    def type(self):
        return 'company' if self.customer != '' else 'private'
    
    @property
    def customer(self):
        return self._customer
    
    @property
    def first_name(self):
        return self._first_name
    
    @property
    def last_name(self):
        return self._last_name
        
    @property
    def phone(self):
        return self._phone
    
    @property
    def email(self):
        return self._email
    
    @property
    def address(self):
        return self._address
    
    @property 
    def postal_code(self):
        return int(self._postal_code) if self._postal_code != '' else ''
    
    @property
    def city(self):
        return self._city
    
    def __repr__(self):
        return 'Customer(kund={}, adress={})'.format(self.kund, self.adress)
    
    def __str__(self):
        return '{};{};{};{};{};{};{};{};{}'.format(self.type, self.customer, self.first_name, self.last_name, self.phone, 
                                          self.email, self.address, self.postal_code, self.city)
