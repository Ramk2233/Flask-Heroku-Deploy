from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.get_by_name(name)
        if store:
            return store.json()
        return {'message': 'store not found'}, 404

    def post(self, name):
        if StoreModel.get_by_name(name):
            return {'message': 'A store with {} already exists'.format(name)}
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured while creating the store'}
        return store.json()

    def delete(self, name):
        store = StoreModel.get_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'store deleted'}
        else:
            return {'message': 'No store with name {}'.format(name)}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
