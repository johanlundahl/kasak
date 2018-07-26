import stats as stats

washes, status = stats.get_todays_washes()
picked_up = len([c for c in washes if c.picked_up == 1])
returned = len([c for c in washes if c.returned == 1])
commented = len([c for c in washes if c.comment != ''])

message = 'Av {} bokade bilar hämtades {} och {} lämnades. {} med kommentarer.'.format(len(washes), picked_up, returned, commented)
stats.post_to_slack(message)
