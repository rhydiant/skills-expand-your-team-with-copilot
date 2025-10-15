"""
MongoDB database configuration and setup for Mergington High School API
"""

from pymongo import MongoClient
from argon2 import PasswordHasher

# Connect to MongoDB with fallback to in-memory storage
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mergington_high']
    activities_collection = db['activities']
    teachers_collection = db['teachers']
    # Test the connection
    client.admin.command('ping')
    USE_MONGODB = True
except Exception as e:
    print(f"MongoDB not available, using in-memory storage: {e}")
    USE_MONGODB = False
    # In-memory fallback storage
    activities_data = {}
    teachers_data = {}
    
    # Create a simple mock collection class
    class MockCollection:
        def __init__(self, data_store):
            self.data = data_store
            
        def find(self, query={}):
            # Simple implementation for basic queries
            results = []
            for key, value in self.data.items():
                if not query or self._matches_query(value, query):
                    results.append({"_id": key, **value})
            return results
                    
        def find_one(self, query):
            for key, value in self.data.items():
                if query.get("_id") == key or self._matches_query(value, query):
                    return {"_id": key, **value}
            return None
            
        def insert_one(self, doc):
            _id = doc.pop("_id")
            self.data[_id] = doc
            return type('Result', (), {'inserted_id': _id})()
            
        def update_one(self, query, update):
            for key, value in self.data.items():
                if query.get("_id") == key or self._matches_query(value, query):
                    if "$push" in update:
                        for field, val in update["$push"].items():
                            if field not in self.data[key]:
                                self.data[key][field] = []
                            self.data[key][field].append(val)
                    if "$pull" in update:
                        for field, val in update["$pull"].items():
                            if field in self.data[key] and val in self.data[key][field]:
                                self.data[key][field].remove(val)
                    return type('Result', (), {'modified_count': 1})()
            return type('Result', (), {'modified_count': 0})()
            
        def count_documents(self, query):
            return len(self.data)
            
        def aggregate(self, pipeline):
            # Basic implementation for the days aggregation
            if len(pipeline) == 3:  # Assume it's the days aggregation
                days = set()
                for activity in self.data.values():
                    if "schedule_details" in activity and "days" in activity["schedule_details"]:
                        days.update(activity["schedule_details"]["days"])
                return [{"_id": day} for day in sorted(days)]
            return []
            
        def _matches_query(self, doc, query):
            for key, value in query.items():
                if key == "schedule_details.days" and isinstance(value, dict) and "$in" in value:
                    if "schedule_details" not in doc or "days" not in doc["schedule_details"]:
                        return False
                    if not any(day in doc["schedule_details"]["days"] for day in value["$in"]):
                        return False
                elif key.startswith("schedule_details.") and isinstance(value, dict):
                    field = key.split(".")[1]
                    if "schedule_details" not in doc or field not in doc["schedule_details"]:
                        return False
                    doc_val = doc["schedule_details"][field]
                    if "$gte" in value and doc_val < value["$gte"]:
                        return False
                    if "$lte" in value and doc_val > value["$lte"]:
                        return False
                elif key in doc and doc[key] != value:
                    return False
            return True
    
    activities_collection = MockCollection(activities_data)
    teachers_collection = MockCollection(teachers_data)

# Methods
def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

def init_database():
    """Initialize database if empty"""

    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})
            
    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one({"_id": teacher["username"], **teacher})

# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"]
    },
    "Manga Maniacs": {
        "description": "Dive into epic adventures, supernatural powers, and heartwarming friendships! Join fellow otaku to discuss your favorite manga series, discover hidden gems, and create your own manga-inspired art. From shonen battles to slice-of-life stories, we celebrate all genres in this ultimate manga sanctuary!",
        "schedule": "Tuesdays, 7:00 PM - 8:30 PM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "19:00",
            "end_time": "20:30"
        },
        "max_participants": 15,
        "participants": []
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
     },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]

