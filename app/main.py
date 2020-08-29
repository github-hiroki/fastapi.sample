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

from typing import Optional
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


def search_on_twitter(keyword: str, count: int):
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

    # ツイートを検索
    contents = []
    contents_length = None
    last_id = None
    while contents_length is None or contents_length != len(contents):
        contents_length = len(contents)
        for tw in tweepy.Cursor(api.search, q=keyword, result_type='recent', max_id=last_id).items(count):
            # ツイートIDを更新
            if last_id is not None and last_id == tw.id:
                continue
            last_id = tw.id
            # リツイートは除外
            if hasattr(tw, 'retweeted_status'):
                continue
            contents.append(TweetContent(tw))
            if count <= len(contents):
                break
            pass
        else:
            continue
        break
    return contents


@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse(
        'template.html',
        {'request': request},
    )


@app.post("/", response_class=HTMLResponse)
async def post_root(request: Request, keyword: str = Form(""), count: int = Form(...)):
    contents = []
    try:
        if keyword:
            contents = search_on_twitter(keyword, count)
            pass
        pass
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

    return templates.TemplateResponse(
        'template.html',
        {'request': request, 'keyword': keyword, 'count': count, 'contents': contents},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
