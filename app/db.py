# -*- coding:utf8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, func
import os
import os.path

engine = create_engine('sqlite:///./meizi.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Meizi(Base):
    __tablename__ = 'meizi'
    id = Column(Integer, primary_key=True,autoincrement=1)
    filename = Column(String(30), unique=True)
    def __init__(self, filename=None):
        self.filename = filename


    def isExist(self):
        db_session.query(self).filter(Meizi.filename == self.filename).first()

    def __repr__(self):
        return '%d:%r' % (self.id , self.filename)

    @staticmethod
    def getRandomN(n):
        res = db_session.query(Meizi).order_by(func.random()).limit(n).all()
#        meizis = {}
#        i =0
#        for item in res:
 #           meizis[i] = res[i].filename
#            i+=1
        return res

class CDN(Base):
    __tablename__ = 'cdn'
    id = Column(Integer, primary_key=True,autoincrement=1)
    cdnurl = Column(String(50), unique=True)
    def __init__(self, url=None):
        self.cdnurl = url

    def __repr__(self):
        return '<CDN %r>' % (self.name)

class ErrorPage(Base):
    __tablename__ = 'errorpage'
    id = Column(Integer, primary_key=True,autoincrement=1)
    view = Column(String(50), unique=True)

    def __init__(self, view=None):
        self.view = view

    def __repr__(self):
        return '<ERRORPAGE %r>' % (self.name)

class ErrDLPic(Base):
    __tablename__ = 'errdlpic'
    id = Column(Integer, primary_key=True,autoincrement=1)
    picurl = Column(String(50), unique=True)

    def __init__(self, picurl=None):
        self.picurl = picurl

    def __repr__(self):
        return '<ErrDLPic %r>' % (self.name)


def init_db():
    Base.metadata.create_all(bind=engine)

def drop_db():
    Base.metadata.drop_all(engine)


def read(rootdir):
    #rootdir = "C:\\Users\\fxre\\Downloads\\meizi" #指明被遍历的文件夹
    counter = 0
    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:                        #输出文件信息
            print filename
            #print "the full name of the file is:" + os.path.join(parent,filename) #输出文件路径信息
            try:
                init_db()
                db_session.add(Meizi(filename))
                counter += 1
                if counter % 100 == 0:
                    db_session.commit()
            except Exception as e:
                print e

try:
    #drop_db()
    init_db()
    db_session.commit()
except Exception as e:
    print e

def DB_ADD(item):
    try:
        db_session.add(item)
        db_session.commit()
    except Exception as e:
        print e
        db_session.rollback()
