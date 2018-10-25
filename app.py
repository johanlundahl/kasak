from flask import Flask 
from flask import send_file
from flask import render_template
import stats as stats
from models import Week
from chart import StackedBar

app = Flask(__name__)

@app.route("/charts/year/<int:year_nbr>/week/<int:week_nbr>", methods=['GET'])
def a_week(year_nbr, week_nbr):
    week = Week(year_nbr, week_nbr)
    weekdays = week.weekdays()
    return week_chart(weekdays, week.number)    
    
    
    #return send_file('charts/{}_{}.png'.format(year_nbr, week_nbr), mimetype='image/png')

@app.route("/charts/current-week", methods=['GET'])
def current_week():
    week = Week.current()
    weekdays = week.weekdays()
    return week_chart(weekdays, week.number)

def week_chart(weekdays, week_nbr):
    days = stats.get_washes_as_list(weekdays)
    week_bookings = list(map(len, days))

    ok = stats.filter_count(days, stats.returned_check)
    commented = stats.filter_count(days, stats.commented_check)
    unknown = stats.filter_count(days, stats.unknown_check)
    traceable = round((sum(ok) + sum(commented)) * 100 / sum(week_bookings))

    chart = StackedBar(title = 'Vecka {}'.format(week_nbr), labels = [d.name() for d in weekdays])
    chart.add_bar('Tvättade', ok, "#34A853")
    chart.add_bar('Kommenterade', commented, "#4285F4")
    chart.add_bar('Okända', unknown, "#8094B7")
    return render_template('week_chart.html', labels=chart.labels, bars=chart.get_bars(), title = chart.title, total=sum(week_bookings), traceable=traceable)
    
if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5010)
