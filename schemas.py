# schemas.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from model import Voyage

class VoyageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Voyage
        load_instance = True  