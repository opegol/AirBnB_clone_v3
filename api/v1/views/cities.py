#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, classes


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_by_state(state_id=None):
    """
        handler for cities route with state_id variable
    """
    st_obj = storage.get('State', state_id)
    if st_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        cities = storage.all('City')
        state_cities = list(obj.to_dict() for obj in cities.values()
                            if obj.state_id == state_id)
        return jsonify(state_cities)

    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        if req.get("name") is None:
            abort(400, 'Missing name')
        City = classes.get("City")
        req['state_id'] = state_id
        new_obj = City(**req)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city_plus_id(city_id=None):
    """handler for cities route with id variable."""
    cty_obj = storage.get('City', city_id)
    if cty_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(cty_obj.to_dict())

    if request.method == 'DELETE':
        cty_obj.delete()
        del cty_obj
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        for k, v in req.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(cty_obj, k, v)
                cty_obj.save()
        return jsonify(cty_obj.to_dict()), 200
