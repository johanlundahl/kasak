import stats as stats

washes, status = stats.get_todays_washes()
message = '{} bilar bokade.'.format(len(washes))
stats.post_to_slack(message)
