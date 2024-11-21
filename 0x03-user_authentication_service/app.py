#!/usr/bin/env python3
""" flask app"""
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """ retunrs payload message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """ registers user """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST', 'DELETE'])
def login_logout():
    """
    creates session
    on successful login
    sets cookie -> session_id
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not AUTH.valid_login(email, password):
            abort(401)
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    elif request.method == 'DELETE':
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)
        AUTH.destroy_session(user.id)
        return redirect("/")


@app.route("/profile")
def profile():
    """
    profile: if exists, 200
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=['POST'])
def reset():
    """
    reset password

    """
    email = request.form.get('email')
    user = AUTH._db.find_user_by(email=email)
    if not user:
        abort(403)
    reset_token = AUTH.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": reset_token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
