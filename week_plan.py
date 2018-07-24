from models import Day, Week
import stats as stats
import locale

#locale.setlocale(locale.LC_ALL, 'sv_SE')

today = Day.today()
week = Week.from_day(today)
weekdays = week.weekdays()

print(weekdays[0], weekdays[-1])
washes = stats.collect_washes(weekdays[0], weekdays[-1])

message = '{} bokningar f  r vecka {}:\n'.format(len(washes), week._number)
for day in weekdays:
    day_nbr = len([w for w in washes if w.date==day.date()])
    message += '{} {}'.format(day.short_name(), day_nbr)
    separator = ', ' if day.next().is_weekday() else ''
    message += separator   

stats.post_to_slack(message)
