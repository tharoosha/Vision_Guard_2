from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Camera, Event, Notification

DATABASE_URL = "sqlite:///cctv_database.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def store_event(camera_id, event_type, timestamp):
    event = Event(camera_id=camera_id, event_type=event_type, timestamp=timestamp)
    session.add(event)
    session.commit()

def store_notification(user_id, event_id, notification_type):
    notification = Notification(user_id=user_id, event_id=event_id, notification_type=notification_type, sent_at=datetime.now(), is_read=0)
    session.add(notification)
    session.commit()
