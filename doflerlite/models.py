from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Text, LargeBinary
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
import time

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    info = Column(Text)
    proto = Column(Text)
    parser = Column(Text)

    def __init__(self, username, password, info, proto, parser):
        self.username = username
        self.password = password
        self.info = info
        self.proto = proto
        self.parser = parser

    def dump(self):
        return {
            'username': self.username,
            'password': self.password,
            'info': self.info,
            'proto': self.proto,
            'parser': self.parser,
        }


class Image(Base):
    __tablename__ = 'images'
    md5sum = Column(Text, primary_key=True)
    timestamp = Column(Integer)
    data = Column(LargeBinary)
    filetype = Column(Text)
    count = Column(Integer)

    def __init__(self, timestamp, filetype, data):
        self.md5sum = md5hash(data)
        self.timestamp = timestamp
        self.filetype = filetype
        self.data = data
        self.count = 1

    def dump(self):
        return {
            'md5sum': self.md5sum,
            'timestamp': self.timestamp,
            'count': self.count,
        }


class Protocol(Base):
    __tablename__ = 'protocols'
    name = Column(Text, primary_key=True)
    stats = relationship('Stat', backref='protocol', 
                         order_by='desc(Stat.timestamp)')

    def __init__(self, name):
        self.name = name

    @hybrid_property
    def total(self):
        '''
        Returns the total number of packets for the given protocol. 
        '''
        count = 0
        for item in self.stats:
            count += item.count
        return count

    def history(self, minutes):
        '''
        Returns the normalized protocol trend for the number of minutes passed.
        '''
        history = []
        cache = int(time.time())
        count = 0
        for item in self.stats:
            if len(history) > minutes:
                break
            if cache - item.timestamp > 60:
                history.append([cache, count])
                cache = item.timestamp
                count = 0
            else:
                count += item.count
        return history


class Stat(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    protocol = Column(Text, ForeignKey('protocols.name'))
    count = Column(Integer)
    timestamp = Column(Integer)
    sensor = Column(Text)

    def __init__(self, protocol, sensor, count):
        self.protocol = protocol
        self.count = count
        self.timestamp = int(time.time())
        self.sensor = sensor


class User(Base):
    __tablename__ = 'users'
    name = Column(Text, primary_key=True)
    password = Column(Text)

    def __init__(self, username, password):
        self.name = username
        self.password = md5hash(password)

    def check(self, password):
        return self.password == md5hash(password):


class Setting(Base):
    __tablename__ = 'settings'
    name = Column(Text, primary_key=True)
    value = Column(Text)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @hybrid_property
    def intvalue(self):
        try:
            return int(self.value)
        except:
            return self.value

    @hybrid_property
    def boolvalue(self):
        try:
            return bool(self.value)
        except:
            return self.value

    @hybrid_property
    def autovalue(self):
        try:
            return bool(self.value)
        except:
            try:
                return int(self.value)
            except:
                return self.value
    