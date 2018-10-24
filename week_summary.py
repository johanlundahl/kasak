from models import Day, Week
import stats as stats
import chart
import slack

def percent(number):
    return int(100*number)

def filter_count(lst, func):
    lst = [list(filter(func, x)) for x in lst]
    return list(map(len, lst))

unknown_check = lambda x: x.returned == 0 and x.comment == ''
commented_check = lambda x: x.returned == 0 and x.comment != ''
returned_check = lambda x: x.returned == 1


def get_bookings_for(weekdays):
    days = []
    for day in weekdays:
        washes, code = stats.get_washes_for(day)
        days.append(washes)
    return days

    
week = Week.current()
weekdays = week.weekdays()

days = get_bookings_for(weekdays)

total = sum(list(map(len, days)))
    
unknown = filter_count(days, unknown_check)
commented = filter_count(days, commented_check)
returned = filter_count(days, returned_check)


x_axis = list(map(lambda x: x.short_name(), weekdays))

chart1 = chart.StackedBar(x_axis)
chart1.add_bar(unknown, 'okända')
chart1.add_bar(commented, 'kommenterade')
chart1.add_bar(returned, 'levererade')
chart1.save('charts/{}_{}.png'.format(week._of_year, week._number))

url = 'http://31.208.165.29:5010/charts/year/{}/week/{}'.format(week._of_year, week._number)

success_rate = percent(sum(returned)/total)
comment_rate = percent(sum(commented)/total)
message = 'Vecka {} tvättades {}% av bokningarna. {}% med kommentar. '.format(week._number, success_rate, comment_rate)

print(message)
#slack.post(message, url)
