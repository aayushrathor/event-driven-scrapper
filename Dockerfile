FROM python:3.9
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8000
CMD [ "python3", "web-scrap.py" ]