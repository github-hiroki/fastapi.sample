# Copyright 2020- hiroki.h Inc.

from fastapi import FastAPI


app = FastAPI(
    title='FastAPIサンプル',
    description='FastAPIサンプルの説明',
    version='0.0.1',
)


@app.get("/")
def read_root():
    return {'Hello': 'World'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
