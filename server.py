from flask import Flask

from relay_lib_seeed import *

app = Flask(__name__)

NUM_RELAY_PORTS = 4


@app.route('/')
def hello_world():
    return 'Hello World!!'


@app.route('/status')
def api_get_status():
    pass


@app.route('/toggle/<port>')
def api_toggle_relay(port):
    relay_toggle_port(port)


@app.route('/on/<port>')
def api_relay_on(port):
    if validate_port(port):
        relay_on(port)


@app.route('/off/<port>')
def api_relay_off(port):
    if validate_port(port):
        relay_off(port)


@app.route('/all_on')
def api_all_on():
    relay_all_on()


@app.route('/all_off')
def api_all_off():
    relay_all_off()


def validate_port(port):
    # Make sure the port falls between 1 and NUM_RELAY_PORTS
    return (port > 0) and (port <= NUM_RELAY_PORTS)
