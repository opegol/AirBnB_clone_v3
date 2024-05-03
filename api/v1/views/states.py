#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, classes


@app_views.route('/states', methods=['GET', 'POST'])
def state_only():
    """
        handler for states route with no id variable
    """
    if request.method == 'GET':
        states = storage.all('State')
        states = list(obj.to_dict() for obj in states.values())
        return jsonify(states)

    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        if req.get("name") is None:
            abort(400, 'Missing name')
        State = classes.get("State")
        new_obj = State(**req)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state_plus_id(state_id=None):
    """handler for states route with id variable."""
    st_obj = storage.get('State', state_id)
    if st_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(st_obj.to_dict())

    if request.method == 'DELETE':
        st_obj.delete()
        del st_obj
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, 'Not a JSON')
        for k, v in req.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(st_obj, k, v)
                st_obj.save()
        return jsonify(st_obj.to_dict())
