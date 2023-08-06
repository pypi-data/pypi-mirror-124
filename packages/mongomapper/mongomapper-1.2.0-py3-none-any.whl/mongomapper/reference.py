import sys
from bson.objectid import ObjectId
from .base import BaseSchema

def Reference(name):
  class _Reference(ObjectId):
    @property
    def model(self):
      if isinstance(name, str):
        return getattr(sys.modules["__main__"], name)
      return name

    @property
    def document(self):
      return self.model.get(self)

    def __repr__(self):
      return f'Reference<{self.model.__name__}>("{self}")'

    @classmethod
    def __get_validators__(cls):
      yield cls.validate
    
    @classmethod
    def validate(cls, v):
      if isinstance(v, BaseSchema):
        v = v._id
      
      return cls(v)
  
  return _Reference

def relationship(name, key):
  @property
  def _func(self):
    model = getattr(sys.modules["__main__"], name)
    filter = {key: self.reference}
    return model.query.where(**filter)
  
  return _func