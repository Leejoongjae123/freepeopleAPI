# coding: utf-8
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db import Base
from db import ENGINE



class PostingTable(Base):
    __tablename__ = 'bigkinds'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    contents=Column(String(10000))
    imageUrl = Column(String(1000))
    regiDate = Column(String(1000))
    category = Column(String(1000))
    urlDetail=Column(String(1000))

class Posting(BaseModel):
    id:int
    title:str
    contents:str
    imageUrl:str
    regiDate:str
    category: str
    urlDetail:str

class FutureTable(Base):
    __tablename__ = 'futurePosting'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    contents=Column(String(10000))
    regiDate = Column(String(1000))
    category=Column(String(1000))


class Future(BaseModel):
    id:int
    title:str
    contents:str
    regiDate:str
    category:str


class ArticleTable(Base):
    __tablename__ = 'columnPosting'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    contents=Column(String(10000))
    category = Column(String(1000))
    regiDate = Column(String(1000))

class Article(BaseModel):
    id:int
    title:str
    contents:str
    category:str
    regiDate:str

class PresidentRealmeterTable(Base):
    __tablename__ = 'presidentrealmeter'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    regiDate=Column(String(1000))
    imageSrc= Column(String(1000))
    url= Column(String(1000))

class PresidentRealmeter(BaseModel):
    id:int
    title:str
    regiDate:str
    imageSrc:str
    url: str

class PresidentNBSTable(Base):
    __tablename__ = 'presidentnbs'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    regiDate=Column(String(1000))
    url= Column(String(1000))
    contents = Column(String(1000))

class PresidentNBS(BaseModel):
    id:int
    title:str
    regiDate:str
    url:str
    contents:str

class gukhimarticleTable(Base):
    __tablename__ = 'gukhimarticle'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    regiDate=Column(String(100))
    category = Column(String(100))
    url= Column(String(1000))


class gukhimarticle(BaseModel):
    id:int
    title:str
    regiDate:str
    category:str
    url:str

class minjuarticleTable(Base):
    __tablename__ = 'minjuarticle'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    regiDate=Column(String(100))
    category = Column(String(100))
    url= Column(String(1000))


class minjuarticle(BaseModel):
    id:int
    title:str
    regiDate:str
    category:str
    url:str

class presidentbriefTable(Base):
    __tablename__ = 'presidentbrief'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    regiDate=Column(String(100))
    url= Column(String(1000))
    contents = Column(String(1000))
    subtitle = Column(String(1000))


class presidentbrief(BaseModel):
    id:int
    title:str
    regiDate:str
    url:str
    contents:str
    subtitle:str

class presidentpressTable(Base):
    __tablename__ = 'presidentpress'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    regiDate=Column(String(100))
    url= Column(String(1000))


class presidentpress(BaseModel):
    id:int
    title:str
    regiDate:str
    url:str

class KDIpolicyTable(Base):
    __tablename__ = 'KDIpolicy'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    regiDate=Column(String(100))
    url= Column(String(1000))
    category=Column(String(1000))
    downloadUrl = Column(String(1000))


class KDIpolicy(BaseModel):
    id:int
    title:str
    regiDate:str
    url:str
    category:str
    downloadUrl:str

class KDIstatusTable(Base):
    __tablename__ = 'KDIstatus'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    regiDate=Column(String(100))
    url= Column(String(1000))
    category=Column(String(1000))
    downloadUrl = Column(String(1000))


class KDIstatus(BaseModel):
    id:int
    title:str
    regiDate:str
    url:str
    category:str
    downloadUrl:str

class yydTable(Base):
    __tablename__ = 'yyd'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    regiDate=Column(String(100))
    url= Column(String(1000))
    category=Column(String(1000))
    downloadUrl=Column(String(1000))


class yyd(BaseModel):
    id:int
    title:str
    regiDate:str
    url:str
    category:str
    downloadUrl:str

class minjuTable(Base):
    __tablename__ = 'minju'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    regiDate=Column(String(100))
    url= Column(String(1000))
    category=Column(String(1000))
    downloadUrl=Column(String(1000))


class minju(BaseModel):
    id:int
    title:str
    regiDate:str
    url:str
    category:str
    downloadUrl:str

class parliamentCreatorTable(Base):
    __tablename__ = 'parliamentCreator'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    regiDate=Column(String(100))
    url= Column(String(1000))
    writer=Column(String(1000))
    downloadUrl=Column(String(1000))


class parliamentCreator(BaseModel):
    id:int
    title:str
    regiDate:str
    url:str
    writer:str
    downloadUrl:str

class KOSISTable(Base):
    __tablename__ = 'KOSIS'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    prev=Column(String(100))
    imageSrc= Column(String(1000))
    category=Column(String(1000))
    value=Column(String(1000))
    year = Column(String(1000))
    unit = Column(String(1000))
    updown=Column(String(1000))
    url = Column(String(1000))


class KOSIS(BaseModel):
    id:int
    title :str
    prev:str
    imageSrc:str
    category:str
    value:str
    year:str
    unit:str
    updown:str
    url:str

class PartyInfo(BaseModel):
    sgId: str
    partyName: str

def main():
    # Table 없으면 생성
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main()