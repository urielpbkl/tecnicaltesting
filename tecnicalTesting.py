import requests
import pandas as pd
from time import time
import hashlib
import json as JSON
import sqlite3
import os


DIR = os.path.dirname(os.path.abspath(__file__))

def request():
    url = 'https://restcountries.com/v2/all'
    response = requests.get(url)
    raw_data = response.json()
    
    return raw_data

def convert_to_hash(text):
      digest = hashlib.sha1(text.encode()).hexdigest()
      return digest


def createDataFrame():
    
    raw_data = request()
    
    region = []
    lenguajes = []
    city_name = []
    time_ejecution = []
    count = -1
    for i in raw_data:
      start_time = time()
      count += 1
      region.append(raw_data[count]['region'])
      city_name.append(raw_data[count]['name'])
      lenguajes.append(convert_to_hash(raw_data[count]['languages'][0]['name']))
      elapsed_time = f'{(time() - start_time) * 1000:.4f}' 
      time_ejecution.append(float(elapsed_time))
    
    
    df = pd.DataFrame(region)
    df.columns = ['Region']
    df['City Name'] = city_name
    df['Language'] = lenguajes
    df['Time'] = time_ejecution
    
    return df

def showData():
    df = createDataFrame()
    print(f"Maximum Time: {df['Time'].max()} ms")
    print(f"Minimum Time: {df['Time'].min()} ms")
    print(f"Average time: {df['Time'].mean()} ms")
    print(f"Total time: {df['Time'].sum()} ms")
    

def dataToSQLite():
    df = createDataFrame()
    conn = sqlite3.connect(rf'{DIR}\base.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data_table(region	TEXT, city_name	TEXT,languaje	TEXT,time TEXT)')
    conn.commit()
    df.to_sql('data_table', conn, if_exists='replace', index = False)
    
    
def dataToJSON():
    df = createDataFrame()
    result = df.to_json(orient="values")
    parsed = JSON.loads(result)
    json = JSON.dumps(parsed, indent=4)  
    json = json.replace("\"", "")
    json = json.replace("\n", "")
                        
    
    with open('data.json', 'w') as file:
        JSON.dump(json, file, indent=4)

    



