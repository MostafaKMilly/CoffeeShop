import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from sqlalchemy.sql.elements import Null

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.order_by(Drink.id).all()
    if len(drinks) == 0:
        abort(404)
    drinksList = [drink.short() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinksList
    }), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.order_by(Drink.id).all()
    #if len(drinks==0) : abort(404)
    drinksDetailList = [drink.long() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinksDetailList
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def insert_drink(payload):
    body = request.get_json()
    req_title = body.get('title')
    req_recipe = body.get('recipe')
    req_recipe = json.dumps(req_recipe)
    try:
        drink = Drink(title=req_title, recipe=req_recipe)
        drink.insert()
        drinksList = [drink.long()]
        return jsonify({
            'success': True,
            'drinks': drinksList
        }), 200
    except:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).first()
    if drink == None:
        abort(404)
    body = request.get_json()
    req_title = body.get('title')
    req_recipe = body.get('recipe')
    req_recipe = json.dumps(req_recipe)
    try:
        drink.title = req_title
        drink.recipe = req_recipe
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).first()
    print(drink)
    if drink == None:
        abort(404)
    try:
        drink.delete()
        return jsonify({
            "success": True,
            "delete": drink_id
        }), 200
    except:
        abort(422)


    # Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'messege': "resource not found"
    }), 404


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'messege': "method not allowed"
    }), 405


@app.errorhandler(422)
def Unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'messege': "Unprocessable Entity"
    }), 422


@app.errorhandler(403)
def Unprocessable(error):
    return jsonify({
        'success': False,
        'error': 403,
        'messege': "premission faild"
    }), 403


@app.errorhandler(401)
def Unprocessable(error):
    return jsonify({
        'success': False,
        'error': 401,
        'messege': "unauthorized"
    }), 401
