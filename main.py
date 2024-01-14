import datetime

from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware
import model
from db import session
from model import PostingTable, Posting,Future,FutureTable,Article,ArticleTable,PresidentRealmeterTable,PresidentRealmeter,PresidentNBS,PresidentNBSTable,gukhimarticle,gukhimarticleTable,minjuarticleTable,minjuarticle,presidentbriefTable,presidentbrief,presidentpressTable,presidentpress,KDIpolicyTable,KDIpolicy,KDIstatusTable,KDIstatus,yydTable,yyd,minjuTable,minju,parliamentCreatorTable,parliamentCreator,KOSISTable,KOSIS,PartyInfo
# from mangum import Mangum
from typing import List, Optional
from sqlalchemy import or_, and_,desc,DateTime,String,Integer,Column,asc
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, HTTPException,Query
from mangum import Mangum
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import re
import json

app = FastAPI() #앱을 생성한다
handler=Mangum(app) #LAMBDA 배포용 MANGUM을 가져온다.

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------API 정의------------
# @app.get("/getProducts")
# def read_users():
#     users = session.query(UserTable).all()
#     return users

def slice_list(lst, start_index):
    return lst[start_index:start_index + 5]

@app.get('/getBigKinds', response_model=List[Posting])
async def read_items(page: Optional[int] = 1):
    postings = session.query(PostingTable)

    sort_column=PostingTable.id
    postings = postings.order_by(sort_column.desc())
    try:
        postings=postings[page-1]
    except:
        postings=[]
        return []
    session.close()
    return [Posting(id=postings.id, title=postings.title, contents=postings.contents,imageUrl=postings.imageUrl,regiDate=postings.regiDate,category=postings.category,urlDetail=postings.urlDetail)]

@app.post("/addBigKinds")
# /user?name="이름"&age=10
async def create_user(postings:List[Posting]):
    for postingData in postings:
        product = PostingTable()
        product.title = postingData.title
        product.contents = postingData.contents
        product.imageUrl = postingData.imageUrl
        product.regiDate = datetime.datetime.now().strftime("%Y-%m-%d")
        product.category = "jgissue"
        product.urlDetail = ""
        session.add(product)
    session.commit()
    session.close()
    return {"status":'success','noPostings':len(postings)}

@app.get('/getFuturePosting', response_model=List[Future])
async def read_items(page: Optional[int] = 1):
    postings = session.query(FutureTable)
    sort_column=FutureTable.regiDate
    postings = postings.order_by(sort_column.desc())
    try:
        postings=slice_list(postings,(page-1)*5)
    except:
        postings=[]
        return []
    session.close()
    return [Future(id=posting.id, title=posting.title, contents=posting.contents,regiDate=posting.regiDate,category=posting.category)for posting in postings]

@app.post("/addFuturePosting")
# /user?name="이름"&age=10
async def create_user(postings:List[Future]):
    print(postings)
    for postingData in postings:
        product = FutureTable()
        product.title = postingData.title
        product.contents = postingData.contents
        product.regiDate = postingData.regiDate
        product.category = postingData.category
        session.add(product)
    session.commit()
    session.close()
    return {"status":'success','noPostings':len(postings)}

@app.get('/getColumnPosting', response_model=List[Article])
async def read_items(page: Optional[int] = 1):
    postings = session.query(ArticleTable)
    sort_column=ArticleTable.regiDate
    postings = postings.order_by(sort_column.desc())
    try:
        postings=slice_list(postings,(page-1)*5)
    except:
        postings=[]
    session.close()
    return [Article(id=posting.id, title=posting.title, contents=posting.contents,regiDate=posting.regiDate,category=posting.category) for posting in postings]

@app.post("/addColumnPosting")
# /user?name="이름"&age=10
async def create_user(postings:List[Article]):
    for postingData in postings:
        product = ArticleTable()
        product.title = postingData.title
        product.contents = postingData.contents
        product.regiDate = postingData.regiDate
        product.category=postingData.category
        session.add(product)
    session.commit()
    session.close()
    return {"status":'success','noPostings':len(postings)}

@app.get('/getPresidentRealmeter', response_model=List[PresidentRealmeter])
async def read_items(page: Optional[int] = 1):
    postings = session.query(PresidentRealmeterTable)
    sort_column=PresidentRealmeterTable.regiDate
    postings = postings.order_by(sort_column.desc())
    try:
        postings=postings[:8]
    except:
        postings=[]
    session.close()
    return [PresidentRealmeter(id=posting.id, title=posting.title, regiDate=posting.regiDate,imageSrc=posting.imageSrc,url=posting.url) for posting in postings]

# @app.post("/addPresdientRealmeter")
# # /user?name="이름"&age=10
# async def create_user(postings:List[PresidentRealmeter]):
#     for postingData in postings:
#         product = PresidentRealmeterTable()
#         product.title = postingData.title
#         product.regiDate = postingData.regiDate
#         product.imageSrc = postingData.imageSrc
#         session.add(product)
#     session.commit()
#     return {"status":'success','noPostings':len(postings)}
@app.post("/addPresdientRealmeter")
async def create_user(postings: List[PresidentRealmeter]):
    added_count = 0
    for postingData in postings:
        # 여기서 기존 데이터베이스에서 regiDate 값이 이미 존재하는지 확인합니다.
        existing_data = session.query(PresidentRealmeterTable).filter_by(url=postingData.url).first()
        if not existing_data:
            # regiDate 값이 중복되지 않는 경우에만 추가합니다.
            product = PresidentRealmeterTable()
            product.title = postingData.title
            product.regiDate = postingData.regiDate
            product.imageSrc = postingData.imageSrc
            product.url = postingData.url
            session.add(product)
            added_count += 1

    session.commit()
    session.close()

    return {"status": "success", "noPostings": added_count}

@app.get('/getPresidentNBS', response_model=List[PresidentNBS])
async def read_items(page: Optional[int] = 1):
    postings = session.query(PresidentNBSTable)
    print('postings:', postings)
    sort_column=PresidentNBSTable.regiDate
    postings = postings.order_by(sort_column.desc())

    try:
        postings=postings[:4]
    except:
        postings=[]
    session.close()
    return [PresidentNBS(id=posting.id, title=posting.title, contents=posting.contents, regiDate=posting.regiDate, url=posting.url) for posting in postings]

@app.post("/addPresdientNBS")
# /user?name="이름"&age=10
async def create_user(postings:List[PresidentNBS]):
    addCount=0
    for postingData in postings:
        existing_data = session.query(PresidentNBSTable).filter_by(url=postingData.url).first()
        if not existing_data:
            product = PresidentNBSTable()
            product.title = postingData.title
            product.regiDate = postingData.regiDate
            product.url = postingData.url
            product.contents=postingData.contents
            session.add(product)
            addCount+=1
    session.commit()
    session.close()
    return {"status":'success','addCount':addCount}

@app.get('/getgukhimarticle', response_model=List[gukhimarticle])
async def read_items(page: Optional[int] = 1):
    postings = session.query(gukhimarticleTable)
    sort_column=gukhimarticleTable.id
    postings = postings.order_by(sort_column.desc())
    postings=postings[:10]
    session.close()
    return [gukhimarticle(id=posting.id, title=posting.title, category=posting.category,regiDate=posting.regiDate,url=posting.url)for posting in postings]

@app.post("/addgukhimarticle")
# /user?name="이름"&age=10
async def create_user(postings:List[gukhimarticle]):
    addCount=0
    for postingData in postings:
        existing_data = session.query(gukhimarticleTable).filter_by(url=postingData.url).first()
        if not existing_data:
            product = gukhimarticleTable()
            product.title = postingData.title
            product.category = postingData.category
            product.regiDate = postingData.regiDate
            product.url = postingData.url
            session.add(product)
            addCount+=1
    session.commit()
    session.close()
    return {"status":'success','addCount':addCount}

@app.get('/getminjuarticle', response_model=List[minjuarticle])
async def read_items(page: Optional[int] = 1):
    postings = session.query(minjuarticleTable)
    sort_column=minjuarticleTable.id
    postings = postings.order_by(sort_column.desc())
    postings=postings[:10]
    session.close()
    return [minjuarticle(id=posting.id, title=posting.title, category=posting.category,regiDate=posting.regiDate,url=posting.url)for posting in postings]

@app.post("/addminjuarticle")
# /user?name="이름"&age=10
async def create_user(postings:List[minjuarticle]):
    addCount=0
    for postingData in postings:
        existing_data = session.query(minjuarticleTable).filter_by(url=postingData.url).first()
        if not existing_data:
            product = minjuarticleTable()
            product.title = postingData.title
            product.category = postingData.category
            product.regiDate = postingData.regiDate
            product.url = postingData.url
            session.add(product)
            addCount+=1
    session.commit()
    session.close()
    return {"status":'success','addCount':addCount}

@app.get('/getpresidentbrief', response_model=List[presidentbrief])
async def read_items(page: Optional[int] = 1):
    postings = session.query(presidentbriefTable)
    sort_column=presidentbriefTable.id
    postings = postings.order_by(sort_column.desc())
    postings=postings[:5]
    session.close()
    return [presidentbrief(id=posting.id, title=posting.title, regiDate=posting.regiDate,url=posting.url,contents=posting.contents,subtitle=posting.subtitle)for posting in postings]

@app.post("/addpresidentbrief")
# /user?name="이름"&age=10
async def create_user(postings:List[presidentbrief]):
    addCount=0
    for postingData in postings:
        existing_data = session.query(presidentbriefTable).filter_by(url=postingData.url).first()
        if not existing_data:
            product = presidentbriefTable()
            product.title = postingData.title
            product.regiDate = postingData.regiDate
            product.url = postingData.url
            product.contents = postingData.contents
            product.subtitle=postingData.subtitle
            session.add(product)
            addCount+=1
    session.commit()
    session.close()
    return {"status":'success','addCount':addCount}

@app.get('/getpresidentpress', response_model=List[presidentpress])
async def read_items(page: Optional[int] = 1):
    postings = session.query(presidentpressTable)
    sort_column=presidentpressTable.regiDate
    postings = postings.order_by(sort_column.desc())
    postings=postings[:5]
    session.close()

    return [presidentpress(id=posting.id, title=posting.title, regiDate=posting.regiDate,url=posting.url)for posting in postings]

@app.post("/addpresidentpress")
# /user?name="이름"&age=10
async def create_user(postings:List[presidentpress]):
    for postingData in postings:
        product = presidentpressTable()
        product.title = postingData.title
        product.regiDate = postingData.regiDate
        product.url = postingData.url
        session.add(product)
    session.commit()
    session.close()
    return {"status":'success','noPostings':len(postings)}

@app.get('/getKDIpolicy', response_model=List[KDIpolicy])
async def read_items(page: Optional[int] = 1):
    postings = session.query(KDIpolicyTable)
    sort_column=KDIpolicyTable.id
    postings = postings.order_by(sort_column.desc())
    postings=postings[:5]
    session.close()
    return [KDIpolicy(id=posting.id, title=posting.title, regiDate=posting.regiDate,url=posting.url,category=posting.category,downloadUrl=posting.downloadUrl)for posting in postings]

@app.post("/addKDIpolicy")
# /user?name="이름"&age=10
async def create_user(postings:List[KDIpolicy]):
    addCount=0
    for postingData in postings:
        existing_data = session.query(KDIpolicyTable).filter_by(url=postingData.url).first()
        if not existing_data:
            product = KDIpolicyTable()
            product.title = postingData.title
            product.regiDate = postingData.regiDate
            product.url = postingData.url
            product.category = postingData.category
            product.downloadUrl = postingData.downloadUrl
            session.add(product)
            addCount+=1
    session.commit()
    session.close()
    return {"status":'success','addCount':addCount}

@app.get('/getKDIstatus', response_model=List[KDIstatus])
async def read_items(page: Optional[int] = 1):
    postings = session.query(KDIstatusTable)
    sort_column=KDIstatusTable.id
    postings = postings.order_by(sort_column.desc())
    postings=postings[:5]
    session.close()
    return [KDIstatus(id=posting.id, title=posting.title, regiDate=posting.regiDate,url=posting.url,category=posting.category,downloadUrl=posting.downloadUrl)for posting in postings]

@app.post("/addKDIstatus")
# /user?name="이름"&age=10
async def create_user(postings:List[KDIstatus]):
    addCount=0
    for postingData in postings:
        existing_data = session.query(KDIstatusTable).filter_by(url=postingData.url).first()
        if not existing_data:
            product = KDIstatusTable()
            product.title = postingData.title
            product.regiDate = postingData.regiDate
            product.url = postingData.url
            product.category = postingData.category
            product.downloadUrl = postingData.downloadUrl
            session.add(product)
            addCount+=1
    session.commit()
    session.close()
    return {"status":'success','addCount':addCount}

@app.get('/getyyd', response_model=List[yyd])
async def read_items(page: Optional[int] = 1):
    postings = session.query(yydTable)
    sort_column=yydTable.id
    postings = postings.order_by(sort_column.desc())
    postings=postings[:5]
    session.close()
    return [yyd(id=posting.id, title=posting.title, regiDate=posting.regiDate,url=posting.url,category=posting.category,downloadUrl=posting.downloadUrl)for posting in postings]

@app.post("/addyyd")
# /user?name="이름"&age=10
async def create_user(postings:List[yyd]):
    addCount=0
    for postingData in postings:
        existing_data = session.query(yydTable).filter_by(url=postingData.url).first()
        if not existing_data:
            product = yydTable()
            product.title = postingData.title
            product.regiDate = postingData.regiDate
            product.url = postingData.url
            product.category = postingData.category
            product.downloadUrl = postingData.downloadUrl
            session.add(product)
            addCount+=1
    session.commit()
    session.close()
    return {"status":'success','addCount':addCount}

@app.get('/getminju', response_model=List[minju])
async def read_items(page: Optional[int] = 1):
    postings = session.query(minjuTable)
    sort_column=minjuTable.id
    postings = postings.order_by(sort_column.desc())
    postings=postings[:5]
    session.close()
    return [minju(id=posting.id, title=posting.title, regiDate=posting.regiDate,url=posting.url,category=posting.category,downloadUrl=posting.downloadUrl)for posting in postings]

@app.post("/addminju")
# /user?name="이름"&age=10
async def create_user(postings:List[minju]):
    for postingData in postings:
        existing_data = session.query(presidentbriefTable).filter_by(url=postingData.url).first()
        if not existing_data:
            product = minjuTable()
            product.title = postingData.title
            product.regiDate = postingData.regiDate
            product.url = postingData.url
            product.category = postingData.category
            product.downloadUrl = postingData.downloadUrl
            session.add(product)
    session.commit()
    session.close()
    return {"status":'success','noPostings':len(postings)}

@app.get('/getParliamentCreator', response_model=List[parliamentCreator])
async def read_items(page: Optional[int] = 1):
    postings = session.query(parliamentCreatorTable)
    sort_column=parliamentCreatorTable.id
    postings = postings.order_by(sort_column.desc())
    postings=postings[:10]
    session.close()

    return [parliamentCreator(id=posting.id, title=posting.title, regiDate=posting.regiDate,url=posting.url,writer=posting.writer,downloadUrl=posting.downloadUrl)for posting in postings]

@app.post("/addParliamentCreator")
async def create_user(postings:List[parliamentCreator]):
    addCount=0
    for postingData in postings:
        existing_data = session.query(parliamentCreatorTable).filter_by(url=postingData.url).first()
        print('existing_data:',existing_data)
        if not existing_data:
            product = parliamentCreatorTable()
            product.title = postingData.title
            product.regiDate = postingData.regiDate
            product.url = postingData.url
            product.writer = postingData.writer
            product.downloadUrl = postingData.downloadUrl
            session.add(product)
            addCount+=1
    session.commit()
    session.close()
    return {"status":'success','addCount':addCount}

@app.get('/getKOSIS', response_model=List[KOSIS])
async def read_items(page: Optional[int] = 1):
    postings = session.query(KOSISTable)
    sort_column=KOSISTable.id
    postings = postings.order_by(sort_column.asc())
    postings=postings
    session.close()
    return [KOSIS(id=posting.id, title=posting.title, prev=posting.prev, imageSrc=posting.imageSrc,category=posting.category,value=posting.value,year=posting.year,unit=posting.unit,updown=posting.updown,url=posting.url)for posting in postings]

#통계청100개 받아오기
@app.get("/getStatistics100/{page}")
async def get_data(page: int):
    # 주어진 페이지 값으로 API 엔드포인트를 생성
    endpoint = f"https://ecos.bok.or.kr/api/KeyStatisticList/5SFKCWM45XWBGE5HVEJ5/json/kr/1/100"
    res=requests.get(endpoint)
    result=json.loads(res.text)['KeyStatisticList']['row']
    result=result[(page-1)*10:page*10]
    # API에 요청을 보내 데이터를 가져오는 코드 작성
    # 이 부분은 requests 또는 httpx 등을 사용하여 구현할 수 있습니다.

    # 예를 들어 requests를 사용하는 경우:
    # import requests
    # response = requests.get(endpoint)
    # data = response.json()

    # 가져온 데이터를 반환
    # return data
    return result

@app.post("/addKOSIS")
# /user?name="이름"&age=10
async def create_user(postings:List[KOSIS]):
    addCount=0
    for postingData in postings:
        existing_data = session.query(KOSISTable).filter_by(title=postingData.title).first()
        if existing_data:

            existing_data.prev = postingData.prev
            existing_data.value = postingData.value
            existing_data.year = postingData.year
            existing_data.unit = postingData.unit
            existing_data.updown = postingData.updown
            existing_data.url = postingData.url

            addCount+=1
    session.commit()
    session.close()
    return {"status":'success','addCount':addCount}

@app.get("/getEconomyStatus")
# /user?name="이름"&age=10
async def create_user():
    cookies = {
        'NNB': 'ECYUUUYBRL2GI',
        'nx_ssl': '2',
        'nid_inf': '-1423366830',
        'NID_AUT': 'iC3ibA0aMSurc1zU0LLE/LUSzu6LbF2JMpDZ7D2MGo9XedYmJrfdmEt/Lr1GG6no',
        'NID_JKL': 'AZLsnOI+EML3GjcMN9gWyVw1+MlMibtLA0S+RJdlWn0=',
        'CBI_SNS': 'naver|sndERqhi1XDkPUc2',
        'NID_SES': 'AAABiMCD0Ef8CngpwSl/A7Gt7tMFh9D8uEVThqE8+qukpgVt0Jrwt3BDmm1YmZF5qAIj5D4k5oqYSLoW9coJ4W5n59YylxlnFPznebxkKuZkcXRGqd8MypgEDwXXGIiIzS5s/iN6zihr6nlxKv0ICLVjwDVz9MbvUMVNj2wxYCPsDzOtmiESJcXXNwiI2/kWWY3W+VyFCnRrSI4Sxq2nfb/pk1EI9hzP9Tb8qosOJfJHZvBN8Tt44PLxVKw6tu3sN4PqZxabOTPH3o9KVywKQdgPBTlRokxuzRrGtGzSqH2ePBdhjnqqqluI7RqNL0YNocbgiP2Opb3rCBd1OIfNGLDB40DvcHOqlwFBhlChPufY1gvojhp7+Vh+P1PieK4cpKjJjnYQorBqk5vwxxo9lzbpl5jqua2zow/ig3HNWmYv/3rVvM5Plao0VI5ljrTtl4t6Ef+K1TupDrVWlbLAPpnDo35QpLRz3p0zMSuCvrG5MsQxnjP6YVEDjoGyz1TZ74W6xbDnl2ITJYS7pLS2UdKw5RM=',
        '_naver_usersession_': 'XOFK3aPVyYRtcPZW0o93aEjC',
        'page_uid': 'ino4mlprvN8ssQ8KMm0sssssttZ-505864',
        'JSESSIONID': 'C15C48480AFC8BE9E1210E439F793F1E',
    }

    headers = {
        'authority': 'finance.naver.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'NNB=ECYUUUYBRL2GI; nx_ssl=2; nid_inf=-1423366830; NID_AUT=iC3ibA0aMSurc1zU0LLE/LUSzu6LbF2JMpDZ7D2MGo9XedYmJrfdmEt/Lr1GG6no; NID_JKL=AZLsnOI+EML3GjcMN9gWyVw1+MlMibtLA0S+RJdlWn0=; CBI_SNS=naver|sndERqhi1XDkPUc2; NID_SES=AAABiMCD0Ef8CngpwSl/A7Gt7tMFh9D8uEVThqE8+qukpgVt0Jrwt3BDmm1YmZF5qAIj5D4k5oqYSLoW9coJ4W5n59YylxlnFPznebxkKuZkcXRGqd8MypgEDwXXGIiIzS5s/iN6zihr6nlxKv0ICLVjwDVz9MbvUMVNj2wxYCPsDzOtmiESJcXXNwiI2/kWWY3W+VyFCnRrSI4Sxq2nfb/pk1EI9hzP9Tb8qosOJfJHZvBN8Tt44PLxVKw6tu3sN4PqZxabOTPH3o9KVywKQdgPBTlRokxuzRrGtGzSqH2ePBdhjnqqqluI7RqNL0YNocbgiP2Opb3rCBd1OIfNGLDB40DvcHOqlwFBhlChPufY1gvojhp7+Vh+P1PieK4cpKjJjnYQorBqk5vwxxo9lzbpl5jqua2zow/ig3HNWmYv/3rVvM5Plao0VI5ljrTtl4t6Ef+K1TupDrVWlbLAPpnDo35QpLRz3p0zMSuCvrG5MsQxnjP6YVEDjoGyz1TZ74W6xbDnl2ITJYS7pLS2UdKw5RM=; _naver_usersession_=XOFK3aPVyYRtcPZW0o93aEjC; page_uid=ino4mlprvN8ssQ8KMm0sssssttZ-505864; JSESSIONID=C15C48480AFC8BE9E1210E439F793F1E',
        'if-modified-since': 'Thu, 07 Sep 2023 17:30:00 GMT',
        'referer': 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%84%A4%EC%9D%B4%EB%B2%84+%EC%A6%9D%EA%B6%8C',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    response = requests.get('https://finance.naver.com/', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text)
    try:
        kospi = soup.find('div', attrs={'class': re.compile('kospi_area group_quot+')}).find("span", attrs={
            'class': 'num'}).get_text()
    except:
        kospi = 0
    print('kospi:',kospi)

    try:
        kospidev=soup.find('div', attrs={'class': re.compile('kospi_area group_quot+')}).find("span", attrs={
            'class': 'num2'}).get_text()
    except:
        kospidev=""
    print("kospidev:",kospidev)
    
    try:
        kospiupdownRaw=soup.find('div', attrs={'class': re.compile('kospi_area group_quot+')}).find("span", attrs={
            'class': re.compile('num_quot+')}).find("span",attrs={'class':'blind'}).get_text()
        if kospiupdownRaw=="+":
            kospiupdown="상승"
        elif kospiupdownRaw=="-":
            kospiupdown="하락"
    except:
        kospiupdown=""
    print("kospiupdown:",kospiupdown)

    try:
        kosdaq = soup.find('div', attrs={'class': re.compile('kosdaq_area group_quot+')}).find("span", attrs={
            'class': 'num'}).get_text()
    except:
        kosdaq = 0
    print('kosdaq:',kosdaq)

    try:
        kosdaqdev=soup.find('div', attrs={'class': re.compile('kosdaq_area group_quot+')}).find("span", attrs={
            'class': 'num2'}).get_text()
    except:
        kosdaqdev=""
    print("kosdaqdev:",kosdaqdev)

    try:
        kosdaqupdownRaw=soup.find('div', attrs={'class': re.compile('kosdaq_area group_quot+')}).find("span", attrs={
            'class': re.compile('num_quot+')}).find("span",attrs={'class':'blind'}).get_text()
        if kosdaqupdownRaw=="+":
            kosdaqupdown="상승"
        elif kosdaqupdownRaw=="-":
            kosdaqupdown="하락"

    except:
        kosdaqupdown=""
    print("kosdaqupdown:",kosdaqupdown)

    try:
        exchange = soup.find_all('div', attrs={'class': 'group1'})[0].find_all("td")[0].get_text()
    except:
        exchange = ""
    print('exchange:',exchange)

    try:
        exchangedev=soup.find_all('div', attrs={'class': 'group1'})[0].find_all("td")[1].get_text().replace("상승","").replace("하락","").replace("보합","").strip()
    except:
        exchangedev=""
    print("exchangedev:",exchangedev)

    try:
        exchangeupdownRaw=soup.find_all('div', attrs={'class': 'group1'})[0].find_all("td")[0].parent['class'][0]
        # print("exchangeupdownRaw:",exchangeupdownRaw,"/ exchangeupdownRaw_TYPE:",type(exchangeupdownRaw),len(exchangeupdownRaw))
        if exchangeupdownRaw.find("up")>=0:
            exchangeupdown="상승"
        elif exchangeupdownRaw.find("down")>=0:
            exchangeupdown="하락"
    except:
        exchangeupdown=""
    print("exchangeupdown:",exchangeupdown)

    try:
        oil = soup.find_all('div', attrs={'class': 'group1'})[1].find_all("td")[0].get_text()
    except:
        oil = ""
    print('oil:',oil)

    try:
        oildev=soup.find_all('div', attrs={'class': 'group1'})[1].find_all("td")[1].get_text().replace("상승","").replace("하락","").replace("보합","").strip()
    except:
        oildev=""
    print("oildev:",oildev)

    try:
        oilupdownRaw=soup.find_all('div', attrs={'class': 'group1'})[1].find_all("td")[0].parent['class'][0]
        if oilupdownRaw.find('up')>=0:
            oilupdown="상승"
        elif oilupdownRaw.find('down')>=0:
            oilupdown="하락"
    except:
        oilupdown=""
    print("oilupdown:",oilupdown)

    try:
        gold = soup.find_all('div', attrs={'class': 'group2'})[1].find_all("td")[0].get_text()
    except:
        gold = ""
    print('gold:',gold)

    try:
        golddev=soup.find_all('div', attrs={'class': 'group2'})[1].find_all("td")[1].get_text().replace("상승","").replace("하락","").replace("보합","").strip()
    except:
        golddev=""
    print("golddev:",golddev)

    try:
        goldupdownRaw=soup.find_all('div', attrs={'class': 'group2'})[1].find_all("td")[0].parent['class'][0]
        if goldupdownRaw.find("up")>=0:
            goldupdown="상승"
        elif goldupdownRaw.find("down")>=0:
            goldupdown="하락"
    except:
        goldupdown=""
    print("goldupdown:",goldupdown)

    try:
        cdinterest = soup.find_all('div', attrs={'class': 'group3'})[0].find_all("td")[0].get_text()
    except:
        cdinterest = ""
    print('cdinterest:',cdinterest)

    try:
        cdinterestdev=soup.find_all('div', attrs={'class': 'group3'})[0].find_all("td")[1].get_text().replace("상승","").replace("하락","").replace("보합","").strip()
    except:
        cdinterestdev=""
    print("cdinterestdev:",cdinterestdev)

    try:
        cdinterestupdownRaw=soup.find_all('div', attrs={'class': 'group3'})[0].find_all("td")[0].parent['class'][0]
        if cdinterestupdownRaw.find("up")>=0:
            cdinterestupdown="상승"
        elif cdinterestupdownRaw.find("down")>=0:
            cdinterestupdown="하락"
        else:
            cdinterestupdown = "보합"
    except:
        cdinterestupdown=""
    print("cdinterestupdown:",cdinterestupdown)

    data={'kospi':kospi,
          'kospidev':kospidev,
          'kospiupdown':kospiupdown,
          "kosdaq":kosdaq,
          'kosdaqdev':kosdaqdev,
          'kosdaqupdown':kosdaqupdown,
          'exchange':exchange,
          'exchangedev':exchangedev,
          'exchangeupdown':exchangeupdown,
          'oil':oil,
          'oildev':oildev,
          'oilupdown':oilupdown,
          'gold':gold,
          'golddev':golddev,
          'goldupdown':goldupdown,
          'cdinterest':cdinterest,
          'cdinterestdev':cdinterestdev,
          'cdinterestupdown':cdinterestupdown
          }

    return data


@app.get('/getKoreaBank')
async def get_items(page: int = Query(1,description="페이지번호"),keyword: str = Query(None, description="필터링할 키워드"),category: str = Query(None, description="필터링할 카테고리")):
    url = 'https://ecos.bok.or.kr/api/KeyStatisticList/5SFKCWM45XWBGE5HVEJ5/json/kr/1/100'
    res = requests.get(url)
    result = json.loads(res.text)['KeyStatisticList']['row']
    # print(result)
    if keyword:
        if category=="카테고리":
            page_items = [item for item in result if keyword.lower() in item["CLASS_NAME"].lower()]
            result = page_items[10 * (page - 1):10 * (page)]
        else:
            page_items = [item for item in result if keyword.lower() in item["KEYSTAT_NAME"].lower()]
            result = page_items[10 * (page - 1):10 * (page)]
    else:
        result = result[10 * (page - 1):10 * (page)]
    return {'data':result,'count':len(result)}

@app.get("/PartyInfo")
async def combine_values(sgId: str ,partyName: str):
    if sgId=="제20대 대통령선거":
        sgIdIndex="20220309"
    elif sgId=="제21대 국회의원선거":
        sgIdIndex="20200415"
    elif sgId=="제19대 대통령선거":
        sgIdIndex="20170509"
    elif sgId=="제20대 국회의원선거":
        sgIdIndex="20160413"
    elif sgId=="제8회 전국동시지방선거":
        sgIdIndex="20220601"
    elif sgId=="제7회 전국동시지방선거":
        sgIdIndex="20180613"
    print('sgIdIndex:',sgIdIndex,partyName.replace(" ",""))
    url = 'http://apis.data.go.kr/9760000/PartyPlcInfoInqireService/getPartyPlcInfoInqire'
    params ={'serviceKey' : 'SY65fkSZc+kXY3+QfVY55nz5CL/qgQiOhs+H8WexkSnCJ9EqBbhPFKgv/13QMrIBBA3Mlsn59Ap9pRF2MaSXkQ==', 'pageNo' : '1', 'numOfRows' : '100', 'sgId' : sgIdIndex, 'partyName' : partyName,'resultType':'json'}
    print(params)

    response = requests.get(url, params=params)
    print(response.text)
    results=json.loads(response.text)['getPartyPlcInfoInqire']['item'][0]


    dataList=[]
    try:
        data1={'title':results['prmsTitle1'],'contents':results['prmmCont1']}
        dataList.append(data1)
    except:
        pass
    try:
        data2={'title':results['prmsTitle2'],'contents':results['prmmCont2']}
        dataList.append(data2)
    except:
        pass
    try:
        data3={'title':results['prmsTitle3'],'contents':results['prmmCont3']}
        dataList.append(data3)
    except:
        pass
    try:
        data4={'title':results['prmsTitle4'],'contents':results['prmmCont4']}
        dataList.append(data4)
    except:
        pass
    try:
        data5={'title':results['prmsTitle5'],'contents':results['prmmCont5']}
        dataList.append(data5)
    except:
        pass
    try:
        data6={'title':results['prmsTitle6'],'contents':results['prmmCont6']}
        dataList.append(data6)
    except:
        pass
    try:
        data7={'title':results['prmsTitle7'],'contents':results['prmmCont7']}
        dataList.append(data7)
    except:
        pass
    try:
        data8={'title':results['prmsTitle8'],'contents':results['prmmCont8']}
        dataList.append(data8)
    except:
        pass
    try:
        data9={'title':results['prmsTitle9'],'contents':results['prmmCont9']}
        dataList.append(data9)
    except:
        pass
    try:
        data10={'title':results['prmsTitle10'],'contents':results['prmmCont10']}
        dataList.append(data10)
    except:
        pass

    return dataList

@app.get("/ElectionResult")
async def ElectionResult(sgName: str ,sdName: str,wiwName: Optional[str] = "강남구"):
    if sgName=="제8회 전국동시지방선거":
        sgId="20220601"
        sgTypecode="3"
    elif sgName=="제20대 대통령선거":
        sgId="20220309"
        sgTypecode = "1"
    elif sgName=="제21대 국회의원선거":
        sgId="20200415"
        sgTypecode = "2"
    if sgName=="제7회 전국동시지방선거":
        sgId="20180613"
        sgTypecode = "3"
    elif sgName=="제19대 대통령선거":
        sgId="20170509"
        sgTypecode = "1"
    elif sgName=="제20대 국회의원선거":
        sgId="20160413"
        sgTypecode = "2"
    elif sgName=="제6회 전국동시지방선거":
        sgId="20140604"
        sgTypecode = "3"
    elif sgName=="제18대 대통령선거":
        sgId="20121219"
        sgTypecode = "1"
    elif sgName=="제19대 국회의원선거":
        sgId="20120411"
        sgTypecode = "2"

    if wiwName==None:
        wiwName=""

    if sgTypecode=="3":
        wiwName=""


    url = 'http://apis.data.go.kr/9760000/VoteXmntckInfoInqireService2/getXmntckSttusInfoInqire'

    if sgName.find("국회의원")>=0:
        params = {'serviceKey': 'SY65fkSZc+kXY3+QfVY55nz5CL/qgQiOhs+H8WexkSnCJ9EqBbhPFKgv/13QMrIBBA3Mlsn59Ap9pRF2MaSXkQ==',
                  'pageNo': '1',
                  'numOfRows': '10',
                  'sgId': sgId,
                  'sgTypecode': sgTypecode, # 1대통령선거 2국회의원선거 3지방선거
                  'sggName': wiwName,
                  'sdName': sdName,
                  'resultType':'json'}
    else:
        params = {'serviceKey': 'SY65fkSZc+kXY3+QfVY55nz5CL/qgQiOhs+H8WexkSnCJ9EqBbhPFKgv/13QMrIBBA3Mlsn59Ap9pRF2MaSXkQ==',
                  'pageNo': '1',
                  'numOfRows': '10',
                  'sgId': sgId,
                  'sgTypecode': sgTypecode, # 1대통령선거 2국회의원선거 3지방선거
                  # 'sggName': '전주시을',
                  'sdName': sdName,
                  'wiwName': wiwName,
                  'resultType':'json'}


    response = requests.get(url, params=params)
    response.raise_for_status()
    print(response.text)
    #필요정보 // 선거인수,유효투표수,정당명,후보자명,특표수

    result=json.loads(response.text)['getXmntckSttusInfoInqire']['item'][0]
    # pprint.pprint(result)
    try:
        totalCount=result['sunsu']
    except:
        totalCount=""
    # print("totalCount:",totalCount)
    try:
        effectiveCount=result['yutusu']
    except:
        effectiveCount=""
    # print('effectiveCount:',effectiveCount)
    try:
        jd1=result['jd01']
    except:
        jd1=""
    try:
        jd2=result['jd02']
    except:
        jd2=""
    try:
        jd3=result['jd03']
    except:
        jd3=""
    try:
        jd4=result['jd04']
    except:
        jd4=""
    try:
        jd5=result['jd05']
    except:
        jd5=""
    try:
        hb1=result['hbj01']
    except:
        hb1=""
    try:
        hb2=result['hbj02']
    except:
        hb2=""
    try:
        hb3=result['hbj03']
    except:
        hb3=""
    try:
        hb4=result['hbj04']
    except:
        hb4=""
    try:
        hb5=result['hbj05']
    except:
        hb5=""
    try:
        dugsu1=result['dugsu01']
    except:
        dugsu1=""
    try:
        dugsu2=result['dugsu02']
    except:
        dugsu2=""
    try:
        dugsu3=result['dugsu03']
    except:
        dugsu3=""
    try:
        dugsu4=result['dugsu04']
    except:
        dugsu4=""
    try:
        dugsu5=result['dugsu05']
    except:
        dugsu5=""
    # print(jd1,hb1,dugsu1,jd2,hb2,dugsu2,jd3,hb3,dugsu3,jd4,hb4,dugsu4,jd5,hb5,dugsu5)
    resultList=[[jd1, hb1, dugsu1], [jd2, hb2, dugsu2], [jd3, hb3, dugsu3], [jd4, hb4, dugsu4], [jd5, hb5, dugsu5]]
    newResultList=[]
    for result in resultList:
        if result[0]!="":
            newResultList.append(result)
    resultList=newResultList

    resultList = sorted(resultList, key=lambda x: int(x[2]), reverse=True)


    #필요정보 // 선거인수,유효투표수,정당명,후보자명,특표수
    data={'totalCount':totalCount,'effectiveCount':effectiveCount,'result':resultList}

    return data

#게시글 모두 가져오기
@app.get("/getAllPostings")
async def getAllPostings(category: int,page:int):
    # 주어진 페이지 값으로 API 엔드포인트를 생성
    if category==0:
        postings1 = session.query(PostingTable)
        sort_column=PostingTable.id
        postings1 = postings1.order_by(sort_column.desc())
    elif category==1:
        postings1 = session.query(FutureTable)
        sort_column = FutureTable.id
        postings1 = postings1.order_by(sort_column.desc())
    elif category==2:
        postings1 = session.query(ArticleTable)
        sort_column = ArticleTable.id
        postings1 = postings1.order_by(sort_column.desc())


    page_size = 5  # 한 페이지에 표시할 게시물 수
    offset = (page - 1) * page_size
    postings_query = postings1.offset(offset).limit(page_size)

    # 쿼리 결과를 리스트로 변환합니다.
    postings = postings_query.all()
    session.close()
    return postings



@app.delete("/removeArticles")
async def delete_users(topic: str, title: str):
    if topic=="bigkinds":
        db=session.query(PostingTable)
    elif topic=="futurePosting":
        db =session.query(FutureTable)
    else:
        db = session.query(ArticleTable)

    # 해당 테이블에서 title이 일치하는 데이터를 가져옴
    existing_data = db.filter_by(title=title).first()

    if existing_data:
        # 데이터가 존재하면 삭제
        db.filter_by(title=title).delete()
        session.commit()
        session.close()
        return {"message": f"Deleted '{title}' from '{topic}' table"}
    else:
        return {"message": f"'{title}' not found in '{topic}' table"}

    # 데이터베이스 세션 시작

@app.get("/getOnePostings")
async def getOnePostings(category: int,id:int):
    # 주어진 페이지 값으로 API 엔드포인트를 생성
    if category==0:
        postings1 = session.query(PostingTable)
        sort_column=PostingTable.regiDate
        postings1 = postings1.order_by(sort_column.desc())
    elif category==1:
        postings1 = session.query(FutureTable)
        sort_column = FutureTable.regiDate
        postings1 = postings1.order_by(sort_column.desc())
    elif category==2:
        postings1 = session.query(ArticleTable)
        sort_column = ArticleTable.regiDate
        postings1 = postings1.order_by(sort_column.desc())

    existing_data = postings1.filter_by(id=id).first()
    session.close()
    return existing_data


# @app.post("/addBigKinds")
# # /user?name="이름"&age=10
# async def create_user(postings:List[Posting]):
#     for postingData in postings:
#         product = PostingTable()
#         product.title = postingData.title
#         product.contents = postingData.contents
#         product.imageUrl = postingData.imageUrl
#         product.regiDate = datetime.datetime.now().strftime("%Y-%m-%d")
#         product.category = "jgissue"
#         product.urlDetail = ""
#         session.add(product)
#     session.commit()
#     session.close()
#     return {"status":'success','noPostings':len(postings)}

# @app.post("/updateOnePosting")
# async def updateOnePosting(category: int,id:int,title:str,contents:str):
#     # 주어진 페이지 값으로 API 엔드포인트를 생성
#     if category==0:
#         postings1 = session.query(PostingTable)
#         sort_column=PostingTable.regiDate
#         postings1 = postings1.order_by(sort_column.desc())
#     elif category==1:
#         postings1 = session.query(FutureTable)
#         sort_column = FutureTable.regiDate
#         postings1 = postings1.order_by(sort_column.desc())
#     elif category==2:
#         postings1 = session.query(ArticleTable)
#         sort_column = ArticleTable.regiDate
#         postings1 = postings1.order_by(sort_column.desc())
#
#     existing_data = postings1.filter_by(id=id).first()
#     if existing_data:
#         existing_data.title=title
#         existing_data.contents=contents
#         session.commit()
#         session.close()
#         result={"result":"update is complete"}
#     else:
#         result = {"result":"update is impossible"}
#
#     return result

@app.post("/updateOnePosting")
async def updateOnePosting(postings:List):
    # 주어진 페이지 값으로 API 엔드포인트를 생성
    print('category:',postings[0]['category'])
    category=int(postings[0]['category'])
    if category==0:
        postings1 = session.query(PostingTable)
        sort_column=PostingTable.regiDate
        postings1 = postings1.order_by(sort_column.desc())
    elif category==1:
        postings1 = session.query(FutureTable)
        sort_column = FutureTable.regiDate
        postings1 = postings1.order_by(sort_column.desc())
    elif category==2:
        postings1 = session.query(ArticleTable)
        sort_column = ArticleTable.regiDate
        postings1 = postings1.order_by(sort_column.desc())

    # 쿼리 결과를 리스트로 변환

    existing_data = postings1.filter_by(id=postings[0]['id']).first()

    print("exsiting_data:",existing_data)
    if existing_data:
        existing_data.title=postings[0]['title']
        existing_data.contents=postings[0]['contents']
        session.commit()
        session.close()
        result={"result":"update is complete"}
    else:
        result = {"result":"update is impossible"}

    return result