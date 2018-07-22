import daily_check as dc

washes, status = dc.get_todays_washes()
message = '{} bilar bokade.'.format(len(washes))
dc.post_to_slack(message)
