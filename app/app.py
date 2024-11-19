import os
import time
from fuzzy_search import FuzzySearcher
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import FUZZY_SEARCH_THRESHOLD

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

# Initialize searcher (no threshold parameter)
searcher = FuzzySearcher()

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
        
        results = list(prizes.find({}))
        for result in results:
            result['_id'] = str(result['_id'])
        
        filtered_results = []
        perfect_matches = []
        
        for prize in results:
            if name and 'laureates' in prize:
                matching_prize = prize.copy()
                matching_laureates = []
                perfect_laureates = []
                
                for laureate in prize['laureates']:
                    full_name = f"{laureate.get('firstname', '')} {laureate.get('surname', '')}".lower()
                    similarity = searcher.calculate_similarity(name, full_name)
                    print(f"Checking name: '{name}' against '{full_name}' - Score: {similarity}")
                    
                    if similarity == 1.0:
                        perfect_laureates.append(laureate)
                    elif similarity > FUZZY_SEARCH_THRESHOLD / 100:
                        matching_laureates.append(laureate)
                
                if perfect_laureates:
                    matching_prize['laureates'] = perfect_laureates
                    perfect_matches.append(matching_prize)
                elif matching_laureates:
                    matching_prize['laureates'] = matching_laureates
                    filtered_results.append(matching_prize)
            
            elif not any([name, category, description]):
                filtered_results.append(prize)
        
        # Return perfect matches if they exist, otherwise return fuzzy matches
        final_results = perfect_matches if perfect_matches else filtered_results
        print(f"Final filtered results count: {len(final_results)}")
        
        return jsonify(final_results)
        
    except Exception as e:
        import traceback
        print(f"Error in search: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)