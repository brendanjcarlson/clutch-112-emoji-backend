from flask import Blueprint, request
from ..models import User, Tweet, Comment, Like

api = Blueprint('api', __name__, url_prefix='/api')


@api.get('/tweets')
def get_tweets():
    tweets = Tweet.query.all()
    if not tweets:
        return {'status': 'not ok', 'message': 'Unable to get tweets'}, 400
    return {'status': 'ok', 'tweets': [tweet.to_dict() for tweet in tweets]}, 200

@api.get('/tweets/<uid>')
def get_user_tweets(uid):
    tweets = Tweet.query.filter_by(user_uid=uid).all()
    if not tweets:
        return {'status': 'not ok', 'message': 'Unable to get tweets'}, 400
    return {'status': 'ok', 'tweets': [tweet.to_dict() for tweet in tweets]}, 200

@api.get('/tweets/<int:id>')
def get_tweet(id):
    tweet = Tweet.query.get(id)
    if not tweet:
        return {'status': 'not ok', 'message': 'Unable to get tweet'}, 400
    return {'status': 'ok', 'tweet': tweet.to_dict()}, 200

@api.post('/tweets')
def create_tweet():
    body = request.json.get('body')
    user_uid = request.json.get('user_uid')
    if not body or not user_uid:
        return {'status': 'not ok', 'message': 'Unable to create tweet'}, 400
    tweet = Tweet(body, user_uid).create()
    return {'status': 'ok', 'tweet': tweet.to_dict()}, 200

@api.delete('/tweets/<int:id>')
def delete_tweet(id):
    tweet = Tweet.query.get(id)
    if not tweet:
        return {'status': 'not ok', 'message': 'Unable to delete tweet'}, 400
    tweet.delete()
    return {'status': 'ok', 'tweet': tweet.to_dict()}, 200

@api.get('/users')
def get_users():
    users = User.query.all()
    if not users:
        return {'status': 'not ok', 'message': 'Unable to get users'}, 400
    return {'status': 'ok', 'users': [user.to_dict() for user in users]}, 200

@api.get('/users/<uid>')
def get_user(id):
    user = User.query.get(uid)
    if not user:
        return {'status': 'not ok', 'message': 'Unable to get user'}, 400
    return {'status': 'ok', 'user': user.to_dict()}, 200

@api.post('/like/<int:id>')
def like_tweet(id):
    tweet = Tweet.query.get(id)
    if not tweet:
        return {'status': 'not ok', 'message': 'Unable to like tweet'}, 400
    like = Like(tweet.id).create()
    return {'status': 'ok', 'like': like.to_dict()}, 200

@api.delete('/like/<int:id>')
def unlike_tweet(id):
    like = Like.query.get(id)
    if not like:
        return {'status': 'not ok', 'message': 'Unable to unlike tweet'}, 400
    like.delete()
    return {'status': 'ok', 'like': like.to_dict()}, 200