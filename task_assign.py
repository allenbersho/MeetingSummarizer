import requests

# Trello API credentials
API_KEY = "API_KEY"
API_TOKEN = "API_TOKEN"
BOARD_ID = "jWZU01CM"  # Replace with your actual Trello board ID

# Dictionary of tasks and assignees
tasks_dict = {
    "Alice": ["Write", "Read"],
    "Bob": ["Study"],
    "Charlie": ["Ask", "Find"]
}

# Trello API endpoints
BASE_URL = "https://api.trello.com/1"
CREATE_CARD_URL = f"{BASE_URL}/cards"
GET_MEMBERS_URL = f"{BASE_URL}/boards/{BOARD_ID}/members"

# Trello list IDs (mapped from your provided JSON)
list_id_map = {
    "Alice": "67c9f4acc7f65a4dbf5fdf4e",
    "Bob": "67c9f4ae464a961d89bb7c74",
    "Charlie": "67c9f4b1531a4b2032dcd2d6"
}

# Step 1: Fetch board members and create a mapping of member names to IDs
response = requests.get(GET_MEMBERS_URL, params={"key": API_KEY, "token": API_TOKEN})

if response.status_code == 200:
    members = response.json()
    member_id_map = {member["fullName"]: member["id"] for member in members}
else:
    print(f"Error fetching members: {response.text}")
    member_id_map = {}

# Step 2: Create Trello cards and assign them correctly
for assignee, tasks in tasks_dict.items():
    for task in tasks:
        card_data = {
            "name": task,
            "idList": list_id_map.get(assignee, ""),  # Assign task to the correct list
            "idMembers": [member_id_map.get(assignee, "")] if assignee in member_id_map else [],  # Assign to the member if found
            "key": API_KEY,
            "token": API_TOKEN
        }

        response = requests.post(CREATE_CARD_URL, json=card_data)

        if response.status_code == 200:
            print(f"✅ Task '{task}' assigned to '{assignee}' successfully!")
        else:
            print(f"❌ Failed to assign task '{task}' to '{assignee}'. Error: {response.text}")
