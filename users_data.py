import json
import os

DATA_FILE = "users.json"

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

users_data = load_users()  # In-memory data

# users_data = {
#     "user1": {
#         "celebrant": "Alice Johnson",
#         "venue": "Rose Garden",
#         "date": "29-June-2025",
#         "guest_count": 100,
#         "budget": 15000,
#     },
#     "user2": {
#         "celebrant": "Bob Smith",
#         "venue": "Beachside Resort",
#         "date": "29-July-2026",
#         "guest_count": 200,
#         "budget": 30000,
#     },
#     "user3": {
#         "celebrant": "Catherine Lee",
#         "venue": "City Hall",
#         "date": "23-August-2025",
#         "guest_count": 50,
#         "budget": 8000,
#     },
#     "user4": {
#         "celebrant": "David Kim",
#         "venue": "Mountain Lodge",
#         "date": "12-October-2025",
#         "guest_count": 150,
#         "budget": 22000,
#     },
#     "user5": {
#         "celebrant": "Eva Martinez",
#         "venue": "Sunset Pavilion",
#         "date": "15-November-2025",
#         "guest_count": 180,
#         "budget": 27000,
#     },
# }
