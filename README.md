# web-scrap-cicd

check deployment at `https://web-scrap.onrender.com/scrap`

![render](https://i.imgur.com/hLN32v6.png)

A python based web scrapper scrapping stocks table from `https://mcxlive.org/` and stores json in mongodb.

## How to Use
- Clone repository ```https://github.com/aayushrathor/web-scrap-cicd.git```
- Build docker image ```docker build -t webscrap-py```
- Run docker image ```docker run -it --rm -p 8000:8000 webscrap-py:latest```
- Go to `http://localhost:8000/docs`

![fastapi-docs](https://i.imgur.com/HDbeCtQ.png)
![](https://i.imgur.com/ownj8Iq.png)
