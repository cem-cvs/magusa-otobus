from models.base import engine, Base
from models.landmarks import Landmark

def init_database():
    Base.metadata.create_all(bind=engine)
