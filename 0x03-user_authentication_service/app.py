#!/usr/bin/env python3
""" Flask module
"""
from flask import Flask, jsonify, request, make_response, abort, redirect
from sqlalchemy.exc import NoResultFound

from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ the home route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """reg user"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({"message": "Missing email or password"}), 400

        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login route"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)

            # Set the session ID as a cookie in the response
            response = make_response(
                jsonify({"email": email, "message": "logged in"}))
            response.set_cookie("session_id", session_id)

            return response

        # Incorrect login information
        return abort(401)

    except NoResultFound:
        # User not found
        return jsonify({"message": "User not found"}), 401


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout route"""
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except NoResultFound as e:
        return jsonify({"response": str(e)}), 403


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Profile route"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return abort(403)
    else:
        return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """get reset password token"""
    email = request.form.get('email')
    uu_id = AUTH.get_reset_password_token(email)
    if uu_id:
        return jsonify({"email": email,
                        "reset_token": uu_id}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """update password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email,
                        "message": "Password updated"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")