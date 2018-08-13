# -*- coding: utf-8 -*- 
import argparse
import time
from models import Day, Week
import stats as stats
import sys

def fetch_bookings(start_day, end_day):
    all_washes = []
    day = start_day
    while day <= end_day:
        washes, code = stats.get_washes_for(day)
        print('Fetched', len(washes), 'for', day)
        all_washes += washes
        time.sleep(1)
        day = day.next()
    print('Fetched', len(all_washes), 'in total')
    return all_washes

def bookings_to_output(bookings, file_suffix):
    with open('report_{}.csv'.format(file_suffix), 'w') as out:
        for booking in bookings:
            out.write(booking.to_csv() +'/n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Will generate a report of booking between two dates')
    parser.add_argument('start_day', type=Day, help='The first day to fetch data from.')
    parser.add_argument('end_day', type=Day, help='The last day to fetch data to.')
    args = parser.parse_args()

    bookings = fetch_bookings(args.start_day, args.end_day)
    bookings_to_output(bookings, '{}-{}'.format(args.start_day, args.end_day))
