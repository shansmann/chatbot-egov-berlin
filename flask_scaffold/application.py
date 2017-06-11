# coding=utf-8

import json
import os
import sys
from datetime import datetime

from flask import Flask, request, __version__, render_template, jsonify

application = Flask(__name__, static_folder='web/static', template_folder='web/templates')
PORT = int(os.getenv('PORT', '8087'))

start_running = datetime.utcnow()
run_with_main = False

#### WEB ###
@application.route('/')
def index():
    return render_template('chat.html')

### End WEB ###

### BOT ###

@application.route('/webhook', methods=['POST'])
def webhook():
    return jsonify(**{'message': {'text': 'I am a sample bot'}, 'ts': datetime.now().isoformat()})

### END BOT ###

@application.route('/main')
def hello():
    import os
    return "Ping " + str(start_running) + ';  Run with main: ' + str(run_with_main) + \
    ', PATH:' + os.environ['PATH']

@application.route('/ver')
def ver():
    return str(sys.version_info)

@application.route('/flaskver')
def fver():
    return str(__version__)

@application.route('/numpyver')
def nver():
    import numpy
    return str(numpy.version.version)

@application.route('/scipyver')
def sver():
    import scipy
    return str(scipy.version.full_version)

@application.route('/pandasver')
def pver():
    import pandas
    return str(pandas.__version__)

@application.route('/sklver')
def sklver():
    import sklearn
    return str(sklearn.__version__)

if __name__ == '__main__':
    run_with_main = True
    application.run(host='0.0.0.0', port=int(PORT), threaded=True, debug=True)
