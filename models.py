# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

class Week:
    def __init__(self, of_year, number):
        self._of_year = of_year
        self._number = number
    
    @classmethod
    def current(self):
        today = Day.today()
        return Week.from_day(today)
        
    @classmethod
    def from_date(self, date):
        return Week(date.year, date.isocalendar()[1])    
    
    @classmethod
    def from_day(self, day):
        return Week.from_date(day.datetime())
    
    @property
    def number(self):
        return self._number
    
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
    
    def __repr__(self):
        return self.short_name()

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

    def status(self):
        if self.returned == 1:
            return 'delivered'
        elif self.comment != '':
            return 'commented'
        else:
            return 'unknown'

    def to_csv(self):
        return '{};{};{};{};{};{};'.format(self.date, self.reg, self.company, self.picked_up, self.returned, self.comment)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.reg, self.date, self.picked_up, self.returned, self.comment)
        
    def __repr__(self):
        return str(self)