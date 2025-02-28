from pymongo import MongoClient

# Local MongoDB URI (default port is 27017)
client = MongoClient("mongodb://127.0.0.1:27017/")

# Access the local DB we created
db = client["MyLocalDB"]

# Check 'Users' collection
print("Users Collection:")
for user in db.Users.find().limit(5):
    print(user)

print("\nPhotoGallery Collection:")
for photo in db.PhotoGallery.find().limit(5):
    print(photo)
