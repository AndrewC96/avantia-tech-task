import os
import time
from fuzzy_search import FuzzySearcher
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

# MongoDB connection with retry
max_retries = 5
retry_delay = 5

for attempt in range(max_retries):
    try:
        mongo_uri = f"mongodb://{os.environ.get('MONGO_USER')}:{os.environ.get('MONGO_PASSWORD')}@mongodb:27017/nobel_db?authSource=admin"
        client = MongoClient(mongo_uri)
        # Test the connection
        client.admin.command('ping')
        db = client['nobel_db']
        prizes = db.prizes
        print("Successfully connected to MongoDB")
        break
    except ConnectionFailure as e:
        if attempt < max_retries - 1:
            print(f"Failed to connect to MongoDB (attempt {attempt + 1}/{max_retries}). Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Failed to connect to MongoDB after all retries")
            raise

# Initialize searcher with lower threshold
searcher = FuzzySearcher(threshold=40)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    try:
        client.admin.command('ping')
        
        name = request.args.get('name', '').lower()
        category = request.args.get('category', '').lower()
        description = request.args.get('description', '').lower()
        
        print(f"\n=== Search Request ===")
        print(f"Parameters: name='{name}', category='{category}', description='{description}'")
        
        # Test if we can get any data at all
        total_count = prizes.count_documents({})
        print(f"Total documents in database: {total_count}")
        
        # Get a sample document to verify structure
        sample = prizes.find_one({})
        print(f"Sample document structure: {sample}")
        
        results = list(prizes.find({}))
        print(f"Initial results count: {len(results)}")
        
        for result in results:
            result['_id'] = str(result['_id'])
        
        filtered_results = []
        for prize in results:
            should_include = False
            
            if name and 'laureates' in prize:
                for laureate in prize['laureates']:
                    full_name = f"{laureate.get('firstname', '')} {laureate.get('surname', '')}".lower()
                    similarity = searcher.calculate_similarity(name, full_name)
                    print(f"Checking name: '{name}' against '{full_name}' - Score: {similarity}")
                    if similarity > 0.40:
                        should_include = True
                        break
            
            if should_include or not any([name, category, description]):
                filtered_results.append(prize)
        
        print(f"Final filtered results: {len(filtered_results)}")
        return jsonify(filtered_results)
        
    except Exception as e:
        import traceback
        print(f"Error in search: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)