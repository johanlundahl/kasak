from models import Day, Week
import stats as stats

def percent(number):
    return int(100*number)
    
today = Day.today()
week = Week.from_day(today)
weekdays = week.weekdays()

week_washes = []
for day in weekdays:
    washes, code = stats.get_washes_for(day)
    week_washes += washes

success = len([w for w in week_washes if w.returned == 1])
success_rate = percent(success/len(week_washes))
comment = len([w for w in week_washes if w.comment != ''])
comment_rate = percent(comment/len(week_washes))
message = 'Vecka {} tvättades {}% av bokningarna. {}% med kommentar. '.format(week._number, success_rate, comment_rate)

stats.post_to_slack(message)
