db = db.getSiblingDB('admin');

db.createUser({
    user: process.env.MONGO_USER,
    pwd: process.env.MONGO_PASSWORD,
    roles: [
        {
            role: "readWrite",
            db: "nobel_db"
        },
        {
            role: "dbAdmin",
            db: "nobel_db"
        }
    ]
});

db = db.getSiblingDB('nobel_db');
db.createCollection('prizes');

// Create indexes for better search performance
db.prizes.createIndex({ "category": 1 });
db.prizes.createIndex({ "year": 1 });
db.prizes.createIndex({ "laureates.firstname": 1 });
db.prizes.createIndex({ "laureates.surname": 1 });