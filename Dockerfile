FROM python:latest
# 標準入出力に関するPythonのバッファリングを無効化し、ログをリアルタイムに出力する
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./ /app

RUN pip install --no-cache-dir -r requirements.txt

ENV OPENAI_API_KEY="833ff2a2381b44ee9155d6a91995565c"

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload" ]

