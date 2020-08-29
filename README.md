# README

FastAPIなるものの存在を[PyConJP 2020](https://pycon.jp/2020/)で知りました。

FastAPIのサンプルを作成してみようとした、、

のですが、途中で楽しくなってFastAPIというよりTwitterAPIのサンプルになってしまいました。

## TwitterAPI

[TwitterAPI](https://developer.twitter.com/en/docs/twitter-api)への登録が必須です。

登録後に取得できる以下の値を .env ファイルに記載してください。

- コンシューマーキー
- コンシューマーシークレットキー
- アクセストークン
- アクセストークンシークレット

~~~console
# cp app/.env.example app/.env
# vi app/.env
~~~

## 実行方法

~~~console
# cd app
# pipenv install
# pipenv run uvicorn main:app --reload
~~~

## 参考

- [FastAPI公式](https://fastapi.tiangolo.com)
- [TwitterAPI](https://developer.twitter.com/en/docs/twitter-api)
- [tweepyドキュメント](https://docs.tweepy.org/en/latest/)
