from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from app.database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    admin = Column(Boolean, default=False, nullable=False)


users = User.__table__

kinds = ('Standart', 'Business', 'President')


class Room(Base):
    __tablename__ = "rooms"
    room_id = Column(Integer, primary_key=True, index=True, unique=True)
    kind = Column("kind", ENUM(*kinds, name="post_kind", create_type=False), nullable=False)
    number_of_beds = Column(Integer)
    price_per_night = Column(Integer)

    users = relationship('UserRoom', backref='rooms', cascade='all,delete')
    photos = relationship('RoomPhoto', backref='rooms', cascade='all,delete')


rooms = Room.__table__


class UserRoom(Base):
    __tablename__ = "user_rooms"
    user_room_id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    room_id = Column(Integer, ForeignKey('rooms.room_id', ondelete='CASCADE'))
    rented_at = Column(DateTime)


user_rooms = UserRoom.__table__


class RoomPhoto(Base):
    __tablename__ = "room_photos"
    photo_id = Column(Integer, primary_key=True, index=True, unique=True)
    kind = Column("kind", ENUM(*kinds, name="post_kind", create_type=False), nullable=False)
    path = Column(String(100), nullable=False)


room_photos = RoomPhoto.__table__
