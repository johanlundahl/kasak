from flask import Flask 
from flask import send_file
from flask import render_template
import stats as stats
from models import Week
from chart import StackedBar

app = Flask(__name__)

@app.route("/charts/year/<int:year_nbr>/week/<int:week_nbr>", methods=['GET'])
def web_root(year_nbr, week_nbr):
    week = Week(year_nbr, week_nbr)
    weekdays = week.weekdays()
    
    
    
    #return send_file('charts/{}_{}.png'.format(year_nbr, week_nbr), mimetype='image/png')

@app.route("/charts/current-week", methods=['GET'])
def current_week():
    week = Week.current()
    weekdays = week.weekdays()

    days = stats.get_washes_as_list(weekdays)
    week_bookings = list(map(len, days))
    
    chart = StackedBar(title = 'Veckans bokningar', labels = [d.name() for d in weekdays])
    chart.add_bar('Tvättade', stats.filter_count(days, stats.returned_check), "#34A853")
    chart.add_bar('Kommenterade', stats.filter_count(days, stats.commented_check), "#4285F4")
    chart.add_bar('Okända', stats.filter_count(days, stats.unknown_check), "#8094B7")
    return render_template('week_chart.html', labels=chart.labels, bars=chart.get_bars(), title = chart.title)
    
if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5010)