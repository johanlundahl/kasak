import stats as stats

washes, status = stats.get_todays_washes()
picked_up = len([c for c in washes if c.picked_up == 1])
returned = len([c for c in washes if c.returned == 1])
commented = len([c for c in washes if c.comment != ''])

message = '{} hämtade, {} lämnade, {} med kommentar '.format(picked_up, returned, commented)
ststs.post_to_slack(message)
