import os
import torch
import whisper
import spacy
import requests
from google import genai
from flask import Flask, request, render_template

client = genai.Client(api_key="AIzaSyAjMaf-yq77LRRnGiNPDIi5oqow8D2I2Eo")

# Initialize Flask app
app = Flask(__name__)

# Ensure uploads folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load AI models
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

torch.cuda.empty_cache()
torch.cuda.ipc_collect()

model = whisper.load_model("medium").to(device).half()
nlp = spacy.load('en_core_web_sm')

# Asana API Credentials
API_KEY = "2/1209600186382960/1209600196537052:2cf8aeba752f534b892566408137e278"
WORKSPACE_ID = "1209600186382972"
PROJECT_ID = "1209600217368759"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_asana_task(task_name, assignee_name):
    """ Creates a task in Asana. """
    user_search_url = "https://app.asana.com/api/1.0/users"
    user_response = requests.get(user_search_url, headers=headers)
    
    if user_response.status_code != 200:
        return f"❌ Error fetching users: {user_response.text}"
    
    user_data = user_response.json()
    assignee_id = next((user["gid"] for user in user_data.get("data", []) if user["name"] == assignee_name), None)

    task_data = {
        "data": {
            "name": task_name,
            "assignee": assignee_id if assignee_id else None,
            "projects": [PROJECT_ID],
            "workspace": WORKSPACE_ID
        }
    }

    response = requests.post("https://app.asana.com/api/1.0/tasks", json=task_data, headers=headers)
    return f"✅ Task '{task_name}' assigned to {assignee_name}!" if response.status_code == 201 else f"❌ Failed to create task. Error: {response.text}"

@app.route("/", methods=["GET"])
def index():
    return render_template("front.html")


@app.route("/page2")
def page2():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "audio" not in request.files:
        return "No file uploaded!", 400

    file = request.files["audio"]
    if file.filename == "":
        return "No selected file!", 400

    # Save the file
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Run Whisper Transcription
    with torch.inference_mode(), torch.autocast(device_type='cuda', dtype=torch.float16):
        result = model.transcribe(file_path)
    response_text = result["text"]

    # Process text into summaries
    sentences = [i for i in nlp(response_text).sents]
    text_chunks_list = []
    max_chunk_size = 1500
    text_chunk = ""
    text_chunk_len = 0

    i = 0
    while i < len(sentences):
        length = len(sentences[i])
        if text_chunk_len + length < max_chunk_size:
            text_chunk_len += length
            text_chunk += str(sentences[i]).strip().replace('\n', '').replace(' ', '')
        else:
            text_chunks_list.append(text_chunk)
            text_chunk = ""
            text_chunk_len = 0
            i -= 12
        i += 1

    text_chunks_list.append(text_chunk)

    summaries = list(map(lambda x: ai_response("Summarize the given text from a meeting giving details of what happened in the meeting and give me the different tasks assigned along with the names to whom it is assigned if mentioned: " + x), text_chunks_list))
    Final_summary_prompt = " ".join(summaries)

    Final_Summary = ai_response("The Given is a chunk of summaries belonging to the same conversation combine the summaries and give the whole final summary as one in a good structured manner with proper spacing and with sufficient paragraphs for the given summaries are: " + Final_summary_prompt)

    # Assign tasks in Asana
    task_results = []
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
            task_results.append(create_asana_task(task_entry["task"], task_entry["assignee"]))

    return render_template("index.html", summary=Final_Summary, task_results=task_results)

def ai_response(text):
    """ Simulated AI response function. Replace with actual AI logic. """
    response = client.models.generate_content(model="gemini-2.0-flash", contents=text)
    return response.text

    

if __name__ == "__main__":
    app.run(debug=True)
