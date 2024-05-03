#!/usr/bin/python3
"""view for User objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, classes


@app_views.route('/users', methods=['GET', 'POST'])
def user_only():
    """
        handler for users route with no id variable
    """
    if request.method == 'GET':
        users = storage.all('User')
        users = list(obj.to_dict() for obj in users.values())
        return jsonify(users)

    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        if req.get("emai") is None:
            abort(400, 'Missing email')
        if req.get("password") is None:
            abort(400, 'Missing passwordi')
        User = classes.get("User")
        new_obj = User(**req)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_plus_id(user_id=None):
    """handler for users route with id variable."""
    us_obj = storage.get('User', user_id)
    if us_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(us_obj.to_dict())

    if request.method == 'DELETE':
        us_obj.delete()
        del us_obj
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        for k, v in req.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(us_obj, k, v)
                us_obj.save()
        return jsonify(us_obj.to_dict())
