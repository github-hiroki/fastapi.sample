# Copyright 2020- hiroki.h Inc.

from fastapi import (
    FastAPI,
    Form,
    HTTPException,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import datetime
import dotenv
import os
import tweepy


app = FastAPI(
    title='FastAPIとTwitterAPIのサンプル',
    description='FastAPIとTwitterAPIを使用したサンプルになります。',
    version='0.0.2',
)
app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


class TweetContent:
    """ツイートの内容を表現する。
    """
    def __init__(self, tweet):
        self.username: str = tweet.user.name
        self.userid: str = tweet.user.id
        self.text: str = tweet.text
        created_at = tweet.created_at + datetime.timedelta(hours=9)
        self.created_at: str = created_at.strftime('%Y-%m-%d %H:%M:%S')
        pass
    pass


def search_on_twitter(keyword: str):
    """ハッシュタグで検索を行う。
    """
    # 環境変数ファイルを読み込む
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    # 認証情報
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret_key = os.getenv('TWITTER_CONSUMER_SECRET_KEY')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    # APIを取得
    api = tweepy.API(auth)

    # ツイートを検索(リツイートは除外する)
    return [
        TweetContent(tw)
        for tw in tweepy.Cursor(api.search, q=keyword, result_type='recent').items(32)
        if not(hasattr(tw, 'retweeted_status'))
    ]


@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse(
        'template.html',
        {'request': request},
    )


@app.post("/", response_class=HTMLResponse)
async def post_root(request: Request, keyword: str = Form(...)):
    try:
        contents = search_on_twitter(keyword)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

    return templates.TemplateResponse(
        'template.html',
        {'request': request, 'keyword': keyword, 'contents': contents},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
