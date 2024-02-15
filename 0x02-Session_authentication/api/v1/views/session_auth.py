#!/usr/bin/env python3
""" Module of session_auth views
"""
from flask import jsonify, request, abort

from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def session_auth():
    """ POST /auth_session/login
    Return:
      - handles route for the session auth
    """
    from api.v1.app import auth
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv("SESSION_NAME"), session_id)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete():
    """delete method"""
    from api.v1.app import auth
    v = auth.destroy_session(request)
    if v is False:
        abort(404)
    else:
        return jsonify({}), 200
