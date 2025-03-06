import torch
import whisper
import spacy
import requests
from google import genai

client = genai.Client(api_key="AIzaSyAjMaf-yq77LRRnGiNPDIi5oqow8D2I2Eo")

def ai_response(text):
    response = client.models.generate_content(model="gemini-2.0-flash", contents=text)
    return response.text

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

torch.cuda.empty_cache()
torch.cuda.ipc_collect()

model = whisper.load_model("medium").to(device).half()

audio_path = "MeetingSummarizer/Reverse Charades - Engaging EVERYONE in a fun Virtual Meeting Game.mp3"

with torch.inference_mode(), torch.autocast(device_type='cuda', dtype=torch.float16):
    result = model.transcribe(audio_path)

response = result["text"]

nlp = spacy.load('en_core_web_sm')
sentences = [i for i in nlp(response).sents]
text_chunks_list = []
max_chunk_size = 1500
text_chunk = ""
text_chunk_len = 0

i=0
while i<len(sentences):
    length = len(sentences[i])
    if text_chunk_len+length<max_chunk_size:
        text_chunk_len+=length
        text_chunk+=str(sentences[i]).strip().replace('\n','').replace('','')
    else:
        text_chunks_list.append(text_chunk)
        text_chunk=""
        text_chunk_len=0
        i-=12
    i+=1

text_chunks_list.append(text_chunk)

summaries = list(map(lambda x: ai_response("Summarize the given text from a meeting giving details of what happened in the meeting and give me the different tasks assigned along with the names to whom it is assigned if mentioned: "+x), text_chunks_list))
Final_summary_prompt = " ".join(summaries)

Final_Summary = ai_response("The Given is a chuck of summaries belonging to the same conversation combine the summaries and give the whole final summary as one in a good structured manner with proper spacing and with sufficient paragraphs for the given summaries are: "+Final_summary_prompt)
print(Final_Summary)

import requests

import requests

# Asana API Credentials
API_KEY = "2/1209600186382960/1209600196537052:2cf8aeba752f534b892566408137e278"
WORKSPACE_ID = "1209600186382972"  # Make sure this is a string
PROJECT_ID = "1209600217368759"    # Make sure this is a string

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_asana_task(task_name, assignee_name):
    # Fetch all users to find the assignee's ID
    user_search_url = "https://app.asana.com/api/1.0/users"
    user_response = requests.get(user_search_url, headers=headers)
    
    if user_response.status_code != 200:
        print(f"❌ Error fetching users: {user_response.text}")
        return
    
    user_data = user_response.json()
    
    assignee_id = None
    for user in user_data.get("data", []):
        if user["name"] == assignee_name:
            assignee_id = user["gid"]
            break

    # If user not found, leave assignee blank
    task_data = {
        "data": {
            "name": task_name,
            "assignee": assignee_id if assignee_id else None,  # Assign if found
            "projects": [str(PROJECT_ID)],  # Ensure GID is a string
            "workspace": str(WORKSPACE_ID)  # Ensure GID is a string
        }
    }

    # Send request to Asana API
    response = requests.post("https://app.asana.com/api/1.0/tasks", json=task_data, headers=headers)

    if response.status_code == 201:
        print(f"✅ Task '{task_name}' assigned to {assignee_name} in Asana!")
    else:
        print(f"❌ Failed to create task. Error: {response.text}")

# Process extracted tasks and assign them in Asana
for task in summaries:
    doc = nlp(task)
    
    tasks = []
    current_name = None

    for ent in doc.ents:
        if ent.label_ == "PERSON": 
            current_name = ent.text
        elif current_name: 
            tasks.append({"assignee": current_name, "task": ent.sent.text})

    for task_entry in tasks:
        create_asana_task(task_entry["task"], task_entry["assignee"])

