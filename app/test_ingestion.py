import os
from pymongo import MongoClient

def verify_data():
    mongo_uri = f"mongodb://{os.environ.get('MONGO_USER')}:{os.environ.get('MONGO_PASSWORD')}@mongodb:27017/nobel_db?authSource=admin"
    client = MongoClient(mongo_uri)
    db = client['nobel_db']
    prizes = db.prizes
    
    # Get total count
    total_prizes = prizes.count_documents({})
    print(f"Total Nobel Prizes stored: {total_prizes}")
    
    # Show a sample prize
    sample = prizes.find_one({})
    if sample:
        print("\nSample Prize Entry:")
        print(f"Year: {sample.get('year')}")
        print(f"Category: {sample.get('category')}")
        if 'laureates' in sample:
            print("Laureates:")
            for laureate in sample['laureates']:
                print(f"- {laureate.get('firstname', '')} {laureate.get('surname', '')}")

if __name__ == "__main__":
    verify_data()