# todo: Implement Signals to notify the app whenever the relay status changes
# todo: use web sockets to update the status display when the relay status changes

from flask import Flask
from flask import Response
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from relay_lib_seeed import *

NUM_RELAY_PORTS = 4

# API responses
success_resp = Response('{msg:"success"}', status=200, mimetype='application/json')
error_resp = Response('{msg:"error"}', status=404, mimetype='application/json')

app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    print("Loading app Main page")
    # return success_resp
    # return render_template('index.html', current_time=datetime.utcnow())
    return render_template('index.html')


@app.route('/status/')
def api_get_status():
    pass
    return success_resp


@app.route('/toggle/<int:port>')
def api_toggle_relay(port):
    relay_toggle_port(port)
    return success_resp


@app.route('/on/<int:port>')
def api_relay_on(port):
    if validate_port(port):
        relay_on(port)
        return success_resp
    else:
        return error_resp


@app.route('/off/<int:port>')
def api_relay_off(port):
    if validate_port(port):
        relay_off(port)
        return success_resp
    else:
        return error_resp


@app.route('/all_on/')
def api_all_on():
    relay_all_on()
    return success_resp


@app.route('/all_off/')
def api_all_off():
    relay_all_off()
    return success_resp


@app.errorhandler(404)
def page_not_found(e):
    print("ERROR: 404")
    return render_template('404.html', the_error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    print("ERROR: 500")
    return render_template('500.html', the_error=e), 500


def validate_port(port):
    # Make sure the port falls between 1 and NUM_RELAY_PORTS
    return (port > 0) and (port <= NUM_RELAY_PORTS)
