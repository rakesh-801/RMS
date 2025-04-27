from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declared_attr

def get_ist_now():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

class TimeStampedModel:
    @declared_attr
    def created_time(cls):
        return Column('createdTime', DateTime(timezone=True), default=get_ist_now)

    @declared_attr
    def last_update_time(cls):
        return Column('lastUpdateTime', DateTime(timezone=True), default=get_ist_now, onupdate=get_ist_now)

    @declared_attr
    def created_by(cls):
        return Column('createdBy', String)

    @declared_attr
    def last_update_by(cls):
        return Column('lastUpdateBy', String)