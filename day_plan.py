import stats as stats

washes, status = stats.get_todays_washes()
assigned = [w for w in washes if w.pickup_assigned and w.return_assigned]
message = 'Idag är {} bilar inbokade varav {} tilldelade.'.format(len(washes), len(assigned))

stats.post_to_slack(message)
