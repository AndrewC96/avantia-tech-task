import os
from pymongo import MongoClient
import requests
import json
from datetime import datetime

def connect_to_mongodb():
    mongo_uri = f"mongodb://{os.environ.get('MONGO_USER')}:{os.environ.get('MONGO_PASSWORD')}@mongodb:27017/nobel_db?authSource=admin"
    client = MongoClient(mongo_uri)
    db = client['nobel_db']
    return db

def fetch_nobel_data():
    # Fetch prizes
    prizes_url = "https://api.nobelprize.org/v1/prize.json"
    prizes_response = requests.get(prizes_url)
    
    # Fetch laureates
    laureates_url = "https://api.nobelprize.org/v1/laureate.json"
    laureates_response = requests.get(laureates_url)
    
    if prizes_response.status_code == 200 and laureates_response.status_code == 200:
        return {
            'prizes': prizes_response.json(),
            'laureates': laureates_response.json()
        }
    else:
        raise Exception(f"Failed to fetch data: Prizes {prizes_response.status_code}, Laureates {laureates_response.status_code}")

def main():
    db = connect_to_mongodb()
    data = fetch_nobel_data()
    
    # Clear existing data
    db.prizes.delete_many({})
    
    # Insert new data
    if 'prizes' in data:
        db.prizes.insert_many(data['prizes']['prizes'])
    
    print("Data ingestion completed successfully!")

if __name__ == "__main__":
    main()