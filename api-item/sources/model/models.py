from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import current_app as app

db = SQLAlchemy()
ma = Marshmallow()


class ItemSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "broadcaster", "category", "price")


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    broadcaster = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)

    # class properties
    _item_schema = ItemSchema()
    _items_schema = ItemSchema(many=True)

    def __repr__(self):
        return f"Item(id= {self.id}, name={self.name}, broadcaster={self.broadcaster}, category={self.category}, price={self.price})"

    @classmethod
    def list_items(cls, order_by=None, **kwargs):
        order_by = order_by or Item.id.desc()
        app.logger.info(f"select items where {kwargs}")
        items = Item.query.filter_by(**kwargs).order_by(order_by).all()
        result = cls._items_schema.dump(items)
        return result

    @classmethod
    def get_item(cls, **kwargs):
        app.logger.info(f"select item where {kwargs}")
        item = Item.query.filter_by(**kwargs).first()
        if not item:
            return None
        result = cls._item_schema.dump(item)
        return result

    @classmethod
    def list_items_by_item_ids(cls, item_ids, order_by=None):
        order_by = order_by or Item.id.desc()
        app.logger.info(f"select items where id in {item_ids}..")
        items = Item.query.filter(Item.id.in_(item_ids)).order_by(order_by).all()
        result = cls._items_schema.dump(items)
        return result
