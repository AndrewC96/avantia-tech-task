from pymongo import MongoClient

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['nobel_db']
    print("MongoDB connected successfully!")
    # List all databases to verify connection
    print("Available databases:", client.list_database_names())
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")