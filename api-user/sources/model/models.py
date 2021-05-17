from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import current_app as app

db = SQLAlchemy()
ma = Marshmallow()


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "access_token")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    access_token = db.Column(db.String, nullable=False)

    # class properties
    _user_schema = UserSchema()
    _users_schema = UserSchema(many=True)

    def __repr__(self):
        return f"User(id= {self.id}, name={self.name}, access_token={self.access_token})"

    @classmethod
    def list_users(cls, order_by=None):
        if not order_by:
            order_by = User.id.desc()
        app.logger.info("retrieving users..")
        users = User.query.filter().order_by(order_by).all()
        result = cls._users_schema.dump(users)
        return result

    @classmethod
    def get_user(cls, **kwargs):
        app.logger.info("retrieving items..")
        user = User.query.filter_by(**kwargs).first()
        result = cls._user_schema.dump(user) if user else None
        return result
