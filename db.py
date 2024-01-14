from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from urllib.parse import quote
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker, declarative_base


# user = "admin" #내꺼
# pwd = "dlwndwo2"
# host = "tutorial.crotgxtzxtks.ap-northeast-2.rds.amazonaws.com"
# port = 3306
# db_url = f'mysql+pymysql://{user}:{quote(pwd)}@{host}:{port}/information?charset=utf8mb4'

user = "admin" #대표님
pwd = "dlwndwo2"
host = "mysql.cg8zdvbjpe3y.ap-northeast-2.rds.amazonaws.com"
port = 3306
db_url = f'mysql+pymysql://{user}:{quote(pwd)}@{host}:{port}/information?charset=utf8mb4'



ENGINE = create_engine(db_url, echo=True)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)


Base = declarative_base()
Base.query = session.query_property()
Base.metadata.create_all(bind=ENGINE)
class Tada(Base):
    __tablename__ = 'tada'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(50))

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<Tada('%s', '%s', '%s')>" % (self.name, self.fullname, self.password)

if __name__ == '__main__':
    #  Database를 없으면 생성 또는 사용의 의미 django에서  create_or_update() (table) 같은것
    Base.metadata.create_all(ENGINE)

    # 세션을 만들어서 연결시킨다.
    Session = sessionmaker()
    Session.configure(bind=ENGINE)
    session = Session()

    # 위의 클래스,인스턴스 변수를 지킨 다음에
    tada = Tada('jay', 'lee joong jae', '1234')

    # 세션에 추가를 한다.
    session.add(tada)
    session.commit()