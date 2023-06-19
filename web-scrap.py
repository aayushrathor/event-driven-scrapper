import os
from os.path import join, dirname
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

app = FastAPI()

load_dotenv(join(dirname(__file__), '.env'))

client = MongoClient(os.getenv("MONGO_URI"), connectTimeoutMS=30000)
db = client["web-scrap"]
collection = db["mcx"]
if collection is not None:
    print("DB Connected!")

@app.on_event("startup")
@repeat_every(seconds=60*60*6, raise_exceptions=True)
async def scrap_table():
    try:
        page = requests.get('https://mcxlive.org/', timeout=30)
        if page.status_code == 200:
            print("https://mcxlive.org/ is live ^_^")
    except Exception as e:
        print(str(e))

    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table', class_='main-table')

    headers = []
    for i in table.thead.find_all('td'):
        title = i.text
        headers.append(title)

    data_rows = []
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text.strip() for i in row_data]
        if row:
            data_rows.append(row)

        mydata = pd.DataFrame(data_rows, columns=headers).dropna()

    data = mydata.to_dict('records')
    if data:
        for item in data:
            symbol = item['Symbol']
            update_data = {
                    '$set': {
                        'Last': item['Last'],
                        'Change': item['Change'],
                        'Change %': item['Change %'],
                        'Close': item['Close'],
                        'High': item['High'],
                        'Low': item['Low'],
                        'Last Trade': item['Last Trade']
                        }
                    }
            collection.update_one({'Symbol': symbol}, update_data, upsert=True)
        print("Data updated in collection!")
    else:
        print("No data found to update!")

def get_version():
    with open('package.json', 'r') as json_file:
        json_data = json.loads(json_file.read())
        version = json_data['version']
        return version

@app.get("/")
def read_root():
    return {
            "name": "web scrapper",
            "version": get_version(),
            "message": "A stocks based web scrapper build with fastapi and beautifulsoup",
            "author": "[aayushrathor](https://github.com/aayushrathor)"
            }

@app.get("/scrap")
def scrap():
    try:
        return list(collection.find({}, {"_id": 0}))
    except:
        return {"Error": "Something went wrong!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", debug=True)
