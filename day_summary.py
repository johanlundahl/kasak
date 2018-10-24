import stats as stats
import slack

washes, status = stats.get_todays_washes()
picked_up = len([c for c in washes if c.picked_up == 1])
returned = len([c for c in washes if c.returned == 1])
commented = [c for c in washes if c.comment != '']

comments = '; ' +', '.join(['_'+c.comment+'_' for c in commented]) if len(commented) else ''
message = 'Av {} bokade bilar hämtades {} och {} lämnades. {} bokningar med kommentarer{}'.format(len(washes), picked_up, returned, len(commented), comments)
slack.post(message)
