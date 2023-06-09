from flask import Blueprint, request
from ..models import db, User, Tweet, Comment, Like
import re


api = Blueprint('api', __name__, url_prefix='/api')


@api.get('/tweets')
def get_tweets():
    tweets = Tweet.query.order_by(Tweet.created_at.desc()).all()
    if not tweets:
        return {'status': 'not ok', 'message': 'Unable to get tweets'}
    return {'status': 'ok', 'tweets': [tweet.to_dict() for tweet in tweets]}

@api.get('/tweets/<uid>')
def get_user_tweets(uid):
    tweets = Tweet.query.filter_by(user_uid=uid).order_by(Tweet.created_at.desc()).all()
    if not tweets:
        return {'status': 'not ok', 'message': 'Unable to get tweets'}
    tweets = [tweet.to_dict() for tweet in tweets]
    return {'status': 'ok', 'tweets': tweets}

@api.get('/tweets/<int:id>')
def get_tweet(id):
    tweet = Tweet.query.get(id)
    if not tweet:
        return {'status': 'not ok', 'message': 'Unable to get tweet'}
    return {'status': 'ok', 'tweet': tweet.to_dict()}

@api.post('/tweets')
def create_tweet():
    user_uid = request.json.get('user_uid')
    body = request.json.get('body')
    user = User.query.filter_by(uid=user_uid).first()
    if not body or not user_uid or not user:
        return {'status': 'not ok', 'message': 'Unable to create tweet'}
    tweet = Tweet(user_uid=user_uid, body=body).create()
    return {'status': 'ok', 'tweet': tweet.to_dict()}

@api.delete('/tweets/<int:id>')
def delete_tweet(id):
    tweet = Tweet.query.get(id)
    if not tweet:
        return {'status': 'not ok', 'message': 'Unable to delete tweet'}
    tweet.delete()
    return {'status': 'ok', 'tweet': tweet.to_dict()}

@api.get('/users')
def get_users():
    users = User.query.all()
    if not users:
        return {'status': 'not ok', 'message': 'Unable to get users'}
    return {'status': 'ok', 'users': [user.to_dict() for user in users]}

@api.get('/users/<uid>')
def get_user(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        return {'status': 'not ok', 'message': 'Unable to get user'}
    return {'status': 'ok', 'user': user.to_dict()}

@api.post('/users')
def create_user():
    uid = request.json.get('uid')
    name = request.json.get('displayName')
    img = request.json.get('photoURL')
    print(img)
    user = User.query.filter_by(uid=uid).first()
    
    if user:
        return {'status': 'ok', 'message': 'Unable to create user. User already exists', 'user': user.to_dict()}
    user = User(uid=uid, name=name, img=img)
    user.create()
    return {'status': 'ok', 'user': user.to_dict()}

# @api.post('/like/<int:id>')
# def like_tweet(id):
#     tweet = Tweet.query.get(id)
#     if not tweet:
#         return {'status': 'not ok', 'message': 'Unable to like tweet'}
#     like = Like(tweet.id).create()
#     return {'status': 'ok', 'like': like.to_dict()}

# @api.delete('/like/<int:id>')
# def unlike_tweet(id):
#     like = Like.query.get(id)
#     if not like:
#         return {'status': 'not ok', 'message': 'Unable to unlike tweet'}
#     like.delete()
#     return {'status': 'ok', 'like': like.to_dict()}