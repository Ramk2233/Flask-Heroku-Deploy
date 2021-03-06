import os 
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import aunthentication, identity
from resources.user import UserRegister
from resources.item import Item, Itemlist
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL","sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'qwerty'
api = Api(app)

jwt = JWT(app, aunthentication, identity)  # /auth --creates new endpoint


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Itemlist, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=4101, debug=True)
