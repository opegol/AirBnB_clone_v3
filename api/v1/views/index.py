#!/usr/bin/python3

"""
creates a route /status on the object app_views that returns a JSON.
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """returns OK status."""
    if request.method == 'GET':
        return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieves the number of each objects by type."""
    if request.method == 'GET':
        resp = {}
        types = {
                    "Amenity": "amenities",
                    "City": "cities",
                    "Place": "places",
                    "Review": "reviews",
                    "State": "states",
                    "User": "users"
                }
        for key, val in types.items():
            resp[val] = storage.count(key)
        return jsonify(resp)
