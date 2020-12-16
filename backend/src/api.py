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

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


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


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


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


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


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


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    body = request.get_json()
    req_title = body.get('title')
    req_recipe = body.get('recipe')
    req_recipe = json.dumps(req_recipe)
    drink = Drink.query.filter(Drink.id == drink_id).first()
    print(drink)
    if drink == None:
        abort(404)
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


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


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
        'messege': "unauthorized"
    }), 403

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
