#!/usr/bin/python3
"""view for Review objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, classes


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews_by_place(place_id=None):
    """
        handler for reviews route with plaice_id variable
    """
    pl_obj = storage.get('Place', place_id)
    if pl_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        reviews = storage.all('Review')
        place_reviews = list(obj.to_dict() for obj in reviews.values()
                             if obj.place_id == place_id)
        return jsonify(place_reviews)

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
        if req.get('text') is None:
            abort(400, 'Missing text')
        Review = classes.get("Review")
        req['place_id'] = place_id
        new_obj = Review(**req)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review_plus_id(review_id=None):
    """handler for reviews route with id variable."""
    rev_obj = storage.get('Review', review_id)
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
            if k not in ['id', 'user_id', 'place_id',
                         'created_at', 'updated_at']:
                setattr(rev_obj, k, v)
                rev_obj.save()
        return jsonify(rev_obj.to_dict()), 200
