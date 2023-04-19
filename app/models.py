from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, unique=True, index=True, primary_key=True)
    uid = db.Column(db.String(128), nullable=False, unique=True, index=True)
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'name': self.name,
        }



class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', backref=db.backref('user', lazy=True))
    comments = db.relationship('Comment', backref='comments', lazy=True)
    likes = db.relationship('Like', backref='likes', lazy=True)

    def __init__(self, body, user_uid):
        self.body = body
        self.user_uid = user_uid

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'created_at': self.created_at,
            'user_uid': self.user_uid,
            'user': self.user.to_dict(),
            'comments': [comment.to_dict() for comment in self.comments],
            'likes': len(self.likes)
        }


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_like', lazy=True))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=False)

    def __init__(self, user_uid, tweet_id):
        self.user_uid = user_uid
        self.tweet_id = tweet_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_user', lazy=True))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=False)

    def __init__(self, body, user_uid, tweet_id):
        self.body = body
        self.user_uid = user_uid
        self.tweet_id = tweet_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'created_at': self.created_at,
            'user_uid': self.user_uid,
            'user': self.user.to_dict(),
            'tweet_id': self.tweet_id
        }