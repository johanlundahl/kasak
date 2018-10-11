from flask import Flask 
from flask import send_file

app = Flask(__name__)

@app.route("/charts/year/<int:year_nbr>/week/<int:week_nbr>", methods=['GET'])
def web_root(year_nbr, week_nbr):
    return send_file('charts/{}_{}.png'.format(year_nbr, week_nbr), mimetype='image/png')
    
if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5010)