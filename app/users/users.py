import boto3
from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.exceptions import abort

from app import logger
from app.conf.config import Config
from app.helper.helper import *

users_bp = Blueprint('users', __name__)

error_pwd_validation_msg = 'Password must contain at least 6 characters, ' \
                           'including Upper/Lowercase, special characters and numbers'


@users_bp.route(Config.USER_PROFILE, methods=['GET'])
@jwt_required
def user_profile(username):
    if get_jwt_identity() == username:
        response = boto3.client('dynamodb', region_name='us-west-2').scan(TableName='Users')
        for usr in response['Items']:
            if usr['username']['S'] == username:
                data = {
                    'name': usr['name']['S'],
                    'email': usr['email']['S'],
                    'dob': usr['dob']['S']
                }
                logger.info(f'User profile details: {data}')
                return make_response(jsonify(data), 200)
    abort(401)


@users_bp.route(Config.DELETE_ACCOUNT, methods=['DELETE'])
@jwt_required
def delete_account(username):
    if get_jwt_identity() == username:
        response = boto3.client('dynamodb', region_name='us-west-2').scan(TableName='Users', Select='SPECIFIC_ATTRIBUTES',
                                                 ProjectionExpression='username')
        for usr in response['Items']:
            if usr['username']['S'] == username:
                boto3.client('dynamodb', region_name='us-west-2').delete_item(
                    Key={
                        'username': {
                            'S': username,
                        },
                    },
                    TableName='Users',
                )
                data = {
                    "success": 'Account Deleted Successfully'
                }
                logger.info(f'User account deleted: {username}')
                return make_response(jsonify(data), 200)
    logger.error(f'Unauthorised access: {username}')
    abort(401)


@users_bp.route(Config.SIGN_IN, methods=['POST'])
def sign_in():
    try:
        response = boto3.client('dynamodb', region_name='us-west-2').scan(TableName='Users')
        for usr in response['Items']:
            if usr['username']['S'] == request.json['username']:
                logger.info(f'Temp Token Generated for user: {request.json["username"]}')
                return make_response(jsonify({
                    'access_token': create_access_token(identity=request.json['username'])
                }), 200)
    except Exception as e:
        data = {
            'error': 'Incorrect Username or Password'
        }
        logger.exception(str(e))
        logger.error(f'Incorrect Username or Password: {request.json["username"]}')
        return make_response(jsonify(data), 401)


@users_bp.route(Config.SIGN_UP, methods=['POST'])
def sign_up():
    try:
        response = boto3.client('dynamodb', region_name='us-west-2').scan(TableName='Users', Select='SPECIFIC_ATTRIBUTES',
                                                 ProjectionExpression='username')
        for usr in response['Items']:
            if usr['username']['S'] == request.json['username']:
                logger.info(f'User already exists: {request.json["username"]}')
                return make_response(jsonify({"username": request.json['username']+' username already exists'}), 400)

        if not email_validation(request.json['email']):
            logger.error(f'Given is not a valid email address: {request.json["email"]}')
            return make_response(jsonify({"email_validation": 'Given is not a valid email address'}), 400)

        if not password_validation(request.json['password']):
            logger.error(f'password validation failed: {request.json["username"]}')
            return make_response(jsonify({"password_validation": error_pwd_validation_msg}), 400)

        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('Users')
        table.put_item(
            Item={
                'username': request.json['username'], 'password': request.json['password'],
                'name': request.json['name'], 'email': request.json['email'], 'dob': request.json['dob'],
            }
        )
    except Exception as e:
        logger.exception(str(e))
        logger.error(f'Unable to sign up: {request.json["username"]}')
        abort(400)
    logger.info('user created successfully.')
    return make_response(jsonify({
        "success": 'User Created Successfully'
    }), 201)
