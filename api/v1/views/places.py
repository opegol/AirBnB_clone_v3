#!/usr/bin/python3

"""view for Place objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, classes


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_by_city(city_id=None):
    """
        handler for places route with plaice_id variable
    """
    cty_obj = storage.get('City', city_id)
    if cty_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        places = storage.all('Place')
        city_places = list(obj.to_dict() for obj in places.values()
                           if obj.city_id == city_id)
        return jsonify(city_places)

    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        user_id = req.get("user_id")
        if user_id is None:
            abort(400, 'Missing user_id')
        usr = storage.get('User', user_id)
        if usr is None:
            abort(404, 'Not found')
        if req.get('name') is None:
            abort(400, 'Missing name')
        Place = classes.get("Place")
        req['city_id'] = city_id
        new_obj = Place(**req)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def place_plus_id(place_id=None):
    """handler for places route with id variable."""
    rev_obj = storage.get('Place', place_id)
    if rev_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(rev_obj.to_dict())

    if request.method == 'DELETE':
        rev_obj.delete()
        del rev_obj
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        for k, v in req.items():
            if k not in ['id', 'user_id', 'city_id',
                         'created_at', 'updated_at']:
                setattr(rev_obj, k, v)
                rev_obj.save()
        return jsonify(rev_obj.to_dict()), 200
