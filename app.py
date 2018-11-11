from flask import Flask 
from flask import send_file
from flask import render_template
import stats as stats
from models import Week
from chart import Chart
from flask_basicauth import BasicAuth
import kasak_params as kp
from OpenSSL import SSL
import os


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = kp.username
app.config['BASIC_AUTH_PASSWORD'] = kp.password

basic_auth = BasicAuth(app)



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
    #chart = StackedBar(title='Dag X', labels=['one', 'two'])
    #chart.add_bar('Ones', [1])
    #return render_template('day.html', labels=chart.labels, bars=chart.get_bars(), title=chart.title)
    return render_template('day.html', labels=['one', 'two'], bars=None, title='Dag X')

@app.route("/overview", methods=['GET'])
@basic_auth.required
def client_overview():
    return render_template('overview.html')

    
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
    return render_template('week_chart.html', labels=chart.labels, bars=chart.get_series(), title = chart.title, total=sum(week_bookings), traceable=traceable)
    
if __name__ == '__main__':    
    context = SSL.Context(SSL.SSLv23_METHOD)
    crt = os.path.join(os.path.dirname(__file__), 'certificate/trycatch.nu.crt')
    key = os.path.join(os.path.dirname(__file__), 'certificate/trycatch.nu.key')
    context = (crt, key)
    app.run(host='0.0.0.0', ssl_context=context, port=443)
