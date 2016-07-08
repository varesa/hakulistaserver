from flask_restful import Resource, reqparse, abort

from models import DBSession
import models


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('order')


class CategoryList(Resource):
    def get(self):
        session = DBSession()
        categories = session.query(models.Category).order_by(models.Category.order.asc()).all()
        return {
            'links': {
                'self': '/categories/'
            },
            'data': {
                'type': 'categories',
                'categories': categories
            }
        }

    def post(self):
        session = DBSession()
        args = parser.parse_args()
        if 'name' not in args.keys():
            abort(400, message="`name` missing")
        if len(args['name']) == 0:
            abort(400, message="`name` empty")
        query = session.query(models.Category).order_by(models.Category.order.desc())
        if query.count():
            order = query.first().order + 1
        else:
            order = 0

        category = models.Category(name=args['name'], order=order)
        session.add(category)
        session.commit()


class Category(Resource):
    def get(self, catid):
        session = DBSession()
        category = session.query(models.Category).filter_by(id=catid).first()
        return category

    def put(self, catid):
        session = DBSession()
        category = session.query(models.Category).filter_by(id=catid).first()
        args = parser.parse_args()
        if args['name'] and len(args['name']):
            category.name = args['name']
        if args['order'] and len(args['order']):
            neworder = args['order']
            other = session.query(models.Category).filter_by(order=neworder).first()
            if other:
                other.order = category.order
                category.order = neworder
        session.commit()

    def delete(self, catid):
        session = DBSession()
        category = session.query(models.Category).filter_by(id=catid).first()
        for item in category.items:
            session.delete(item)
        session.delete(category)
        session.commit()


class ItemList(Resource):
    def get(self, catid):
        session = DBSession()
        category = session.query(models.Category).filter_by(id=catid).first()
        items = sorted(category.items, key=lambda x: x.name)
        return {
            'links': {
                'self': '/categories/{}/items/'.format(catid),
                'category': '/categories/{}'.format(catid)
            },
            'data': {
                'type': 'items',
                'items': items
            }
        }
    
    def post(self, catid):
        session = DBSession()
        args = parser.parse_args()
        if 'name' not in args.keys():
            abort(400, message="`name` missing")
        if len(args['name']) == 0:
            abort(400, message="`name` empty")
        category = session.query(models.Category).filter_by(id=catid).first()
        item = models.Item(category=category, name=args['name'])
        session.add(item)
        session.commit()


class Item(Resource):
    def get(self, catid, itemid):
        session = DBSession()
        item = session.query(models.Item).filter_by(id=itemid).first()
        return item

    def delete(self, catid, itemid):
        session = DBSession()
        item = session.query(models.Item).filter_by(id=itemid).first()
        session.delete(item)
        session.commit()
