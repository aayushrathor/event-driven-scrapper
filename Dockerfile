FROM python:3.8.9-slim-buster as pythonBuilder
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y build-essential libxml2-dev libxslt-dev && \
    pip install --no-cache-dir --user -r requirements.txt

FROM python:3.8.9-slim-buster
WORKDIR /app
COPY --from=pythonBuilder /root/.local /root/.local
COPY . /app
ENV PATH=/root/.local/bin:$PATH
CMD [ "uvicorn", "web-scrap:app", "--reload" ]
