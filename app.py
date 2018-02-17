from flask import Flask, Response
from flask_sse import sse
from Store import *
from flask import request
import os

app = Flask(__name__)

app.config["REDIS_URL"] = os.environ["REDIS_URL"]
store = Store(app.config.get("REDIS_URL"))


app.register_blueprint(sse, url_prefix='/beaconinfo_stream')


@app.route('/visible_beacons', methods=["POST"])
def update_current_beacons():
    data = request.get_data()
    store.set_current_beacons(data)

    next_beacon = store.get_nearest_beacon()
    content = store.get_beacon_info(next_beacon)
    sse.publish(content, type='display_update')

    return "Beacon data successfully stored"


@app.route('/visible_beacons', methods=["GET"])
def get_current_beacons():
    data = store.get_current_beacons()
    return as_json(data)


@app.route("/beacons")
def get_all_beacons():
    data = store.get_all_beacons()
    return as_json(data)


@app.route("/beacon/<beacon_id>")
def get_beacon_info(beacon_id):
    data = store.get_beacon_info(beacon_id)
    return as_json(data)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


def as_json(data):
    return Response(response=data, mimetype='application/json')