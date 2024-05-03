#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, classes


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenity_only():
    """
        handler for amenities route with no id variable
    """
    if request.method == 'GET':
        amenities = storage.all('Amenity')
        amenities = list(obj.to_dict() for obj in amenities.values())
        return jsonify(amenities)

    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        if req.get("name") is None:
            abort(400, 'Missing name')
        Amenity = classes.get("Amenity")
        new_obj = Amenity(**req)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_plus_id(amenity_id=None):
    """handler for amenities route with id variable."""
    amn_obj = storage.get('Amenity', amenity_id)
    if amn_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(amn_obj.to_dict())

    if request.method == 'DELETE':
        amn_obj.delete()
        del amn_obj
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        for k, v in req.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amn_obj, k, v)
                amn_obj.save()
        return jsonify(amn_obj.to_dict())
