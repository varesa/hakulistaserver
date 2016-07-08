
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()
DBSession = sessionmaker()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    order = Column(Integer)

    def to_serializable(self):
        return {
            'links': {
                'self': '/categories/{}'.format(self.id),
                'items': '/categories/{}/items/'.format(self.id),
            },
            'data': {
                'type': 'category',
                'id': self.id,
                'name': self.name,
                'order': self.order
            }
        }


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", backref="items")

    def to_serializable(self):
        return {
            'links': {
                'category': '/categories/{}'.format(self.category_id),
                'self': '/categories/{}/items/{}'.format(self.category_id, self.id)
            },
            'data': {
                'type': 'item',
                'id': self.id,
                'name': self.name
            }
        }
