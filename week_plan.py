from models import Day, Week
import stats as stats
import locale

#locale.setlocale(locale.LC_ALL, 'sv_SE')

today = Day.today()
week = Week.from_day(today)
weekdays = week.weekdays()

message = 'Bokningar för vecka {}:\n'.format(week._number)
for day in weekdays:
    washes, code = stats.get_washes_for(day)
    message += '{} {} bilar\n'.format(day.name(), len(washes))

stats.post_to_slack(message)
