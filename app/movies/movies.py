import logging
import uuid

import boto3
from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import abort
from app import logger
from app.conf.config import Config

movies_bp = Blueprint('movies', __name__)


@movies_bp.route(Config.FETCH_MOVIES, methods=['GET'])
@jwt_required
def fetch_movies(username):
    movie_list = []
    if get_jwt_identity() == username:
        response = boto3.client('dynamodb', region_name='us-west-2').scan(TableName='Movies', Select='SPECIFIC_ATTRIBUTES',
                                                 ProjectionExpression='username, title')
        for movie in response['Items']:
            if movie['username']['S'] == username:
                movie_list.append(movie['title']['S']) if movie['title']['S'] not in movie_list else None
        logger.info(f'Found Movies: {movie_list}')
        return make_response(jsonify(movie_list), 200)
    else:
        logger.error('Unauthorised access. Unable to fetch movies.')
        abort(401)


@movies_bp.route(Config.DELETE_MOVIE, methods=['DELETE'])
@jwt_required
def delete_movie(username, title):
    if get_jwt_identity() == username:
        response = boto3.client('dynamodb', region_name='us-west-2').scan(
            TableName='Movies', Select='SPECIFIC_ATTRIBUTES', ProjectionExpression='id, username, title')
        for movie in response['Items']:
            if movie['username']['S'] == username and movie['title']['S'] == title:
                boto3.client('dynamodb', region_name='us-west-2').delete_item(
                    Key={
                        'id': {
                            'S': movie['id']['S'],
                        },
                    },
                    TableName='Movies',
                )
        return make_response(jsonify({
            "success": 'Movie Deleted Successfully'
        }), 200)
    else:
        logger.error('Unauthorised access. Unable to delete movie.')
        abort(401)


@movies_bp.route(Config.ADD_MOVIE, methods=['POST'])
@jwt_required
def add_movie(username):
    if get_jwt_identity() == username:
        try:
            dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
            table = dynamodb.Table('Movies')
            table.put_item(
                Item={
                    'id': str(uuid.uuid4()),
                    'username': username,
                    'title': request.json.get('title'),
                    'movie_type': request.json.get('movie_type'),
                    'description': request.json.get('description'),
                    'cast': request.json.get('cast'),
                    'genres': request.json.get('genres'),
                    'production': request.json.get('production'),
                    'country': request.json.get('country')
                }
            )
        except KeyError:
            logger.error('Unauthorised access. Unable to add a movie.')
            abort(400)

        return make_response(jsonify({
            "success": 'Movies Added Successfully'
        }), 201)
    else:
        logger.error('Unauthorised access. Unable to add a movie.')
        abort(401)


@movies_bp.errorhandler(400)
def invalid_request(error):
    logger.error(f'Invalid Request: {error}')
    return make_response(jsonify({'error': f'Invalid Request {error}'}))


@movies_bp.errorhandler(404)
def not_found(error):
    logger.error(f'Movie Not Found: {error}')
    return make_response(jsonify({'error': 'Movie not found'}), 404)


@movies_bp.errorhandler(401)
def unauthorized(error):
    logger.error(f'Unauthorised access: {error}')
    return make_response(jsonify({'error': 'Unauthorized Access'}), 401)
