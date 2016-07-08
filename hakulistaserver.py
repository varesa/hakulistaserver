import os

from flask import Flask
from flask_restful import Api
from sqlalchemy.engine import create_engine

from custjson import CustJSONEncoder
from models import Base, DBSession
from resources import Category, Item, CategoryList, ItemList


class Config:
    RESTFUL_JSON = {'cls': CustJSONEncoder}


# Flask
app = Flask(__name__)
app.config.from_object(Config)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Flask-RESTful
api = Api(app)

# SQLAlchemy
engine = create_engine('sqlite:///var/www/hakulistaserver/hakulistaserver.sqlite', echo=True)
DBSession.configure(bind=engine)
Base.metadata.create_all(engine)

# REST routes
api.add_resource(CategoryList, "/categories/")
api.add_resource(Category, "/categories/<int:catid>")

api.add_resource(ItemList, "/categories/<int:catid>/items/")
api.add_resource(Item, "/categories/<int:catid>/items/<int:itemid>")


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    debug = 'debug' in os.environ.keys()
    app.run(host="0.0.0.0", debug=debug)
