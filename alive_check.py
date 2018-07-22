import daily_check as dc

washes, status = dc.get_todays_washes()
if status is not 200:
    dc.post_to_slack('app.kasak.se svarar inte på tilltal.')
#else:
#    dc.post_to_slack('everything is fine :)')
