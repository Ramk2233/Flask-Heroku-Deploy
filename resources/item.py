import sqlite3
from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left empty"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item need a store id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_by_name(name)
        if item:
            return item.json()

        return {"message": "Item does not exist"}

    def post(self, name):
        if ItemModel.get_by_name(name):
            return {'message': 'an item with {} already exists'.format(name)}

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred during inserting an item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.get_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': 'item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.get_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class Itemlist(Resource):
    def get(self):

        return {"Items": [item.json() for item in ItemModel.query.all()]}
