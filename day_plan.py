import stats as stats

washes, status = stats.get_todays_washes()
message = 'Idag är {} bilar inbokade.'.format(len(washes))
stats.post_to_slack(message)
