import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

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
    try:
        drinks = Drink.query.all()
    except Exception as e:
        print(e)
        abort(404)
    
    if drinks == None:
        abort(404)
    
    drinksShort = [drink.short() for drink in drinks]

    return jsonify ({
        'success': True,
        'drinks': drinksShort
    })
    

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
    try:
        drinks = Drink.query.all()
    except Exception as e:
        print(e)
        abort(404)
    
    if drinks == None:
        abort(404)
    
    drinksLong = [drink.long() for drink in drinks]

    return jsonify ({
        'success': True,
        'drinks': drinksLong
    })
    


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
def create_drinks(payload):
    body = request.get_json()
 
    if not body:
        abort(400)

    new_recipe = json.dumps(body.get('recipe'))
    new_title = body.get('title')

    try:
        new_drink = Drink(title=new_title,recipe=new_recipe)
        new_drink.insert()
  
    except Exception as e:
        print(e)
        abort(422)


    return jsonify({
        'success': True,
        'drinks': new_drink.long()
    })

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

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(payload,id):

    try:
        drink = Drink.query.filter(Drink.id==id).one_or_none()
    except Exception as e:
        print(e)
        abort(404)

    if not drink:
        abort(401)
    
    body = request.get_json()

    if not body:
        abort(400)
    
    bad_request = True

    if "title" in body:
        drink.title = body['title']
        bad_request = False

    if "recipe" in body:
        drink.recipe = body['recipe']
        bad_request = False

    if bad_request is True:
        abort(400)

    try:
        drink.insert()
    except Exception as e:
        print(e)
        abort(400)

    return jsonify({
        'success': True,
        'drinks': drink.long()
    })


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

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload,id):
    try:
        drink = Drink.query.filter(Drink.id==id).one_or_none()
    except Exception as e:
        print(e)
        abort(404)

    if not drink:
        abort(404)

    try:
        drink.delete()
    except Exception as e:
        print(e)
        abort(500)
    
    return jsonify({
        'success': True,
        'delete': id
    })


# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

@app.errorhandler(AuthError)
def auth_error(error):
    message = error.error['description']
    
    return jsonify({
        "success": False,
        "error": 401,
        "message": message
    }), 401
    



if __name__ == "__main__":
    app.run(debug=True)