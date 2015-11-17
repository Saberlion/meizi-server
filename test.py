from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
engine = create_engine('sqlite:///./db/meizi.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Meizi(Base):
    __tablename__ = 'meizi'
    id = Column(Integer, primary_key=True, autoincrement=1)
    filename = Column(String(30), unique=True)

    def __init__(self, filename=None):
        self.filename = filename

    def __repr__(self):
        return '<User %r>' % (self.name)

class CDN(Base):
    __tablename__ = 'cdn'
    id = Column(Integer, primary_key=True, autoincrement=1)
    cdnurl = Column(String(50), unique=True)

    def __init__(self, url=None):
        self.cdnurl = url

    def __repr__(self):
        return '<CDN %r>' % (self.name)
def init_db():
    Base.metadata.create_all(bind=engine)

def drop_db():
    Base.metadata.drop_all(engine)
try:
    init_db()
    db_session.merge(Meizi('adfadfgw3erfds'))
    db_session.merge(CDN('http://mycdn.com/'))
    db_session.commit()
except Exception as e:
    print e
