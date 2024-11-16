#!/usr/bin/env python3
""" Module of sesssion_auth
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def auth_session():
    email = request.form.get('email')
    passsword = request.form.get("password")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if passsword is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(passsword):
        return jsonify({"error": "wrong password"}), 404
    else:
        from api.v1.app import auth
        key = auth.create_session(user[0].id)
        out = jsonify(user[0].to_json())
        out.set_cookie(getenv("SESSION_NAME"), key)
        return out