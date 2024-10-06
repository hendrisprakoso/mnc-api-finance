from functools import wraps
from datetime import datetime
from flask import request, jsonify

from settings import app
from database import get_detail_account_by_token


def authorization_control(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        """ Getting header request """
        content_type = request.headers.get('Content-Type', None)
        token = request.headers.get('Authorization', None)

        if token in ["", None]:
            return jsonify({"status" : False, "message" : "Token is missing!"}), 411
        
        if content_type in ["", None] and content_type != "application/json":
            return jsonify({"status" : False, "message" : "Content_type is not valid!"}), 400


        token_split = token.split(" ")[1]
        account_detail = get_detail_account_by_token(token_split)            
        if not account_detail:
            return jsonify({"status" : False, "message" : "Unauthenticated!"}), 401
        
        return f(*args, **kwargs)
    return wrapper