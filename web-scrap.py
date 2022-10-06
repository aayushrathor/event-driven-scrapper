import os
from os.path import join, dirname
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = MongoClient()
client = MongoClient("mongodb+srv://admin:1234@web-scrap.4lwt3mh.mongodb.net/?retryWrites=true&w=majority")
db = client["web-scrap"]
collection = db["mcx"]
print("DB Connected!")

def scrap_table():
    page = requests.get('https://mcxlive.org/', verify=False, timeout=10)
    print("MCX page status:", page)

    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table', class_='main-table')

    headers = []
    for i in table.thead.find_all('td'):
        title = i.text
        headers.append(title)

    mydata = pd.DataFrame(columns=headers)

    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        
        if(row != ['']):
            symbol = row[0].strip()
            last = row[1].strip()
            change = row[2].strip()
            changePer = row[3].strip()
            close = row[4].strip()
            high = row[5].strip()
            low = row[6].strip()
            lastTrade = row[7].strip()
        
        mydata = mydata.append({'Symbol': symbol, 'Last': last, 'Change': change, 'Change %': changePer, 'Close': close, 'High': high, 'Low': low, 'Last Trade': lastTrade}, ignore_index=True)

    drop_collection = collection.drop()
    print("Collection dropped!")
    
    ins_collection = collection.insert_many(mydata.to_dict('records'))
    print("Data inserted in collection!")

scrap_table()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/scrap")
def scrap():
    try:
        return list(collection.find({}, {"_id": 0}))
    except:
        return {"Error": "Something went wrong!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)