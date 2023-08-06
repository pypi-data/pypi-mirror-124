import inspect
from typing import Type
from bson.objectid import ObjectId
from . import BaseSchema

def relationship(name, key):
  caller = inspect.currentframe().f_back

  @property
  def _func(self):
    model = caller.f_globals[name]
    filter = {key: self.reference}
    return model.query.where(**filter)
  
  return _func

def Reference(schema):
  caller = inspect.currentframe().f_back

  class _Reference(ObjectId):
    @property
    def model(self) -> Type[BaseSchema]:
      if isinstance(schema, str):
        return caller.f_globals[schema]
      return schema

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