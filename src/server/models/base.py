from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

"""
class de Base pour définir les conventions de nommage et autres éléments à appliquer sur tous les objets utilisant cette classe comme 
Base sqlAlchemy
"""
class Base(DeclarativeBase):
    """
    définit les conventions de nommage des tables et clées liées aux objets en BDD
    """
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })
