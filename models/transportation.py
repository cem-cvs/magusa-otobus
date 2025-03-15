from sqlalchemy import Column, Integer, String, Float
from models.base import Base

class TransportRoute(Base):
    __tablename__ = "transport_routes"

    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String, index=True)
    start_lat = Column(Float)
    start_lng = Column(Float)
    end_lat = Column(Float)
    end_lng = Column(Float)

    def to_dict(self):
        return {
            "id": self.id,
            "route_name": self.route_name,
            "start_lat": self.start_lat,
            "start_lng": self.start_lng,
            "end_lat": self.end_lat,
            "end_lng": self.end_lng,
        }
