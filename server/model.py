from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Initialize the database engine and session
DATABASE_URL = "sqlite:///cctv_database.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Define User and Camera models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    device_token = Column(String)

class Camera(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    rtsp_url = Column(String)
    last_seen = Column(DateTime)

# Define Event, Notification, and UserCamera models
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"))
    timestamp = Column(DateTime)
    event_type = Column(String)
    event_details = Column(String)
    
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    notification_type = Column(String)
    sent_at = Column(DateTime)
    is_read = Column(Integer)

# Establish database tables
Base.metadata.create_all(engine)

# Function to store an event in the database
def store_event(camera_id, event_type, timestamp):
    event = Event(camera_id=camera_id, event_type=event_type, timestamp=timestamp)
    session.add(event)
    session.commit()

# Function to store a notification in the database
def store_notification(user_id, event_id, notification_type):
    notification = Notification(user_id=user_id, event_id=event_id, notification_type=notification_type, sent_at=datetime.now(), is_read=0)
    session.add(notification)
    session.commit()

if __name__ == "__main__":
    # Example usage
    user = User(username="user1", email="user1@example.com", password_hash="hashed_password", device_token="device_token_user1")
    session.add(user)
    session.commit()

    camera = Camera(name="Living Room", location="Front", rtsp_url="rtsp://camera_url", last_seen=datetime.now())
    session.add(camera)
    session.commit()

    store_event(camera_id=camera.id, event_type="Intrusion Detected", timestamp=datetime.now())
    store_notification(user_id=user.id, event_id=1, notification_type="Intrusion Alert")
