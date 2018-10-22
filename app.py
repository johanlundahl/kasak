from flask import Flask 
from flask import send_file
from flask import render_template
import stats as stats
from models import Week

app = Flask(__name__)

@app.route("/charts/year/<int:year_nbr>/week/<int:week_nbr>", methods=['GET'])
def web_root(year_nbr, week_nbr):
    return send_file('charts/{}_{}.png'.format(year_nbr, week_nbr), mimetype='image/png')

@app.route("/charts/current", methods=['GET'])
def current_week():
    week = Week.current()
    weekdays = week.weekdays()

    days = []
    for day in weekdays:
        washes, code = stats.get_washes_for(day)
        days.append(washes)
    week_bookings = list(map(len, days))
    return render_template('week_chart.html', labels=['må', 'ti', 'on', 'to', 'fr'], values=week_bookings, title='Chart')
    
if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5010)