from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Text, LargeBinary, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func
import time
from dofler.md5 import md5hash

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
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'info': self.info,
            'proto': self.proto,
            'parser': self.parser,
        }


class Image(Base):
    __tablename__ = 'images'
    md5sum = Column(String(32), primary_key=True)
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


class Stat(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    proto = Column(Text)
    count = Column(Integer)
    timestamp = Column(Integer)
    user = Column(Text)

    def __init__(self, protocol, username, count):
        self.proto = protocol
        self.count = count
        self.timestamp = int(time.time()) - (int(time.time()) % 60)
        self.user = username


class User(Base):
    __tablename__ = 'users'
    name = Column(String(32), primary_key=True)
    password = Column(String(32))

    def __init__(self, username, password):
        self.name = username
        self.update(password)

    def update(self, password):
        self.password = md5hash(password)

    def check(self, password):
        return self.password == md5hash(password)


class Setting(Base):
    __tablename__ = 'settings'
    name = Column(String(128), primary_key=True)
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
            return bool(int(self.value))
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


class Reset(Base):
    __tablename__ = 'resets'
    id = Column(Integer, primary_key=True)
    type = Column(Text)
    timestamp = Column(Integer)

    def __init__(self, datatype):
        self.type = datatype
        self.timestamp = int(time.time())