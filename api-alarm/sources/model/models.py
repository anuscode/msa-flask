from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import current_app as app

db = SQLAlchemy()
ma = Marshmallow()


class AlarmSchema(ma.Schema):
    class Meta:
        fields = ("id", "item_id", "user_id", "created")


class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)

    # class properties
    _alarm_schema = AlarmSchema()
    _alarms_schema = AlarmSchema(many=True)

    def __repr__(self):
        return f"Item(id= {self.id}, item_id={self.item_id}, user_id={self.user_id}, created={self.created})"

    @classmethod
    def list_user_alarmed_items(cls, order_by=None, **kwargs):
        order_by = order_by or Alarm.id.desc()
        app.logger.info(f"select alarm_items where {kwargs}")
        alarm_items = Alarm.query.filter_by(**kwargs).order_by(order_by).all()
        result = cls._alarms_schema.dump(alarm_items)
        return result

    @classmethod
    def insert_alarm_item(cls, user_id=None, item_id=None):
        if not user_id or not item_id:
            raise ValueError("user_id and item_id are required value..")
        is_alarm_exist = Alarm.query.filter_by(user_id=user_id, item_id=item_id).first()
        if is_alarm_exist:
            return

        created = datetime.now()
        alarm = Alarm(user_id=user_id, item_id=item_id, created=created)
        db.session.add(alarm)

    @classmethod
    def delete_alarm_item(cls, **kwargs):
        alarm = Alarm.query.filter_by(**kwargs).first_or_404()
        db.session.delete(alarm)
