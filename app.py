from chart import Chart
from flask import Flask, render_template, url_for, redirect, send_file
from flask_basicauth import BasicAuth
import kasak_params as kp
from models import Week
import stats as stats
from OpenSSL import SSL
import os
import sys

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = kp.username
app.config['BASIC_AUTH_PASSWORD'] = kp.password
basic_auth = BasicAuth(app)

@app.route("/", methods=['GET'])
@basic_auth.required
def root():
    return redirect(url_for('overview'))

@app.route("/charts/year/<int:year_nbr>/week/<int:week_nbr>", methods=['GET'])
@basic_auth.required
def a_week(year_nbr, week_nbr):
    week = Week(year_nbr, week_nbr)
    weekdays = week.weekdays()
    return week_chart(weekdays, week.number)    
    
@app.route("/weeks/current", methods=['GET'])
@basic_auth.required
def current_week():
    week = Week.current()
    weekdays = week.weekdays()
    return week_chart(weekdays, week.number)

@app.route("/days/current", methods=['GET'])
@basic_auth.required
def current_day():
    chart = Chart(title='Dag X', labels=['one', 'two', 'three'])
    washes, http_code = stats.get_todays_washes()
    ok, commented, unknown = filtered_count(washes)
    chart.add_serie('Tvättade', ok, "#4BC0C0")
    chart.add_serie('Kommenterade', commented, "#36A2EB")
    chart.add_serie('Okända', unknown, "#FF6384")
    return render_template('day.html', series_names=chart.series_names(), bars=chart.get_series(), title=chart.title)

@app.route("/overview", methods=['GET'])
@basic_auth.required
def overview():
    cars = []
    washes, http_code = stats.get_todays_washes()
    cars = [(x.reg, x.pickup_time[:5], x.return_time[:5]) for x in washes]
    return render_template('overview.html', title='Översikt', cars = cars)

    
def week_chart(weekdays, week_nbr):
    days = stats.get_washes_as_list(weekdays)
    week_bookings = list(map(len, days))

    ok = stats.filter_count(days, stats.returned_check)
    commented = stats.filter_count(days, stats.commented_check)
    unknown = stats.filter_count(days, stats.unknown_check)
    traceable = round((sum(ok) + sum(commented)) * 100 / sum(week_bookings))

    chart = Chart(title = 'Vecka {}'.format(week_nbr), labels = [d.name() for d in weekdays])
    chart.add_serie('Tvättade', ok, "#4BC0C0")
    chart.add_serie('Kommenterade', commented, "#36A2EB")
    chart.add_serie('Okända', unknown, "#FF6384")
    return render_template('week.html', labels=chart.labels, bars=chart.get_series(), title = chart.title, total=sum(week_bookings), traceable=traceable)

def filtered_count(lst):
    ok = len(list(filter(stats.returned_check, lst)))
    commented = len(list(filter(stats.commented_check, lst)))
    unknown = len(list(filter(stats.unknown_check, lst)))
    return ok, commented, unknown
    
if __name__ == '__main__':    
    if 'win32' in sys.platform:
        app.run(host='0.0.0.0')
    else:
        context = SSL.Context(SSL.SSLv23_METHOD)
        crt = os.path.join(os.path.dirname(__file__), 'certificate/trycatch.nu.crt')
        key = os.path.join(os.path.dirname(__file__), 'certificate/trycatch.nu.key')
        context = (crt, key)
        app.run(host='0.0.0.0', ssl_context=context, port=443)
