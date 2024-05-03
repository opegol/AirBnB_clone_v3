#!/usr/bin/python3
"""Flask App for Airbnb_clone_v3 project."""

from flask import Flask, jsonify, render_template, make_response, url_for
from flask_cors import CORS, cross_origin
from api.v1.views import app_views
from models import storage
import os

# Flask server
app = Flask(__name__)

app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """calls .close() on current SQLAlchemy Session."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors."""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def handle_400(exception):
    """Alternatively handles 400 errros."""
    err_code = exception.__str__().split()[0]
    desc = exception.description
    msg = {'error': desc}
    return make_response(jsonify(msg), err_code)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', 5000),
            threaded=True)
