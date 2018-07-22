import stats as stats
import threading
from datetime import datetime, timedelta
from models import Day
import requests
import kasak_params as kp

one_day = 86400
one_hour = 3600

def daily_status_check():
    threading.Timer(one_day, daily_status_check).start()
    
    if Day.today().is_weekday():
        print('Running status check')
        washes, status = get_todays_washes()
        summary = summarize_washes(washes)
        post_to_slack(summary)
        
def post_to_slack(message):
    payload = {"text": "{}".format(message)}
    r = requests.post(url = kp.slack_webhook_url, json = payload)
    print(r.status_code, r.text)

def get_todays_washes():
    today = Day.today()
    return stats.get_washes_for(today)
    
def summarize_washes(washes):
    picked_up = len([c for c in washes if c.picked_up == 1])
    returned = len([c for c in washes if c.returned == 1])
    commented = len([c for c in washes if c.comment != ''])
    date = washes[0].date
    return '{} bilar {} varav {} med kommentar ({} hämtade, {} lämnade)'.format(len(washes), date, commented, picked_up, returned)
           
if __name__ == '__main__':
    now = datetime.now()
    five_oclock = datetime.now().replace(hour=16, minute=0, second=0)
    sleep = timedelta(days=1)-(now - five_oclock) if five_oclock<now else five_oclock - now
    threading.Timer(sleep.seconds, daily_status_check).start()
