from openai import OpenAI
import os.path
import datetime
from dotenv import load_dotenv
import json
import requests
from flask import Flask, request, abort, jsonify

# Load environment variables
load_dotenv()
API_KEY = os.getenv("LLM_API_KEY")
SMS_API_KEY = os.getenv("SMS_API_KEY")
SMS_DEVICE_ID = os.getenv("SMS_DEVICE_ID")

# Load configuration from config.json
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
context = config["context"]
model = config["model"]
base_url = config["base_url"]
rules = "\n".join(config["rules"])
auth_numbers = config["auth_numbers"]

# Initialize the AI client
client = OpenAI(api_key=API_KEY, base_url=base_url)
path = os.path.dirname(os.path.abspath(__file__))
_done = False

# Initialize Flask app
app = Flask(__name__)

# Base URL for SMS API
sms_base_url = 'https://api.textbee.dev/api/v1'

# Ensure the conversation history directory exists
history_dir = os.path.join(path, "conv_history")
if not os.path.exists(history_dir):
    os.makedirs(history_dir)

# Function to create a log entry
def logger(status, content):
    completePath = os.path.join(path, "main.log")
    with open(completePath, "r") as file:
        currentContent = file.read()
    with open(completePath, "w") as file:
        file.write(f"{datetime.datetime.now()} - {status} : {content}\n{currentContent}")

# Function to edit the history of a conversation
def edit_history(number, date, role, message):
    completePath = os.path.join(path, "conv_history/", f"{number}.json")
    entry = {
        "role": role,
        "content": f" [{date.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    }
    if os.path.isfile(completePath):
        with open(completePath, "r") as file:
            history = json.load(file)
    else:
        history = {
            "history": []
        }
    history["history"].append(entry)
    with open(completePath, "w") as file:
        json.dump(history, file, indent=4)
        file.close()

# Function to get the history of a conversation
def get_history(number):
    completePath = os.path.join(path, "conv_history/", f"{number}.json")
    if os.path.isfile(completePath):
        with open(completePath, "r") as file:
            return json.load(file)["history"]
    return []

# Function to check if a number is authorized to chat
def check_auth(number):
    for auth_number in auth_numbers:
        if number == auth_number:
            return True
    return False

# Function to ask the AI a question
def ask_ai(number, message):
    messages = [
        {"role": "system",
            "content": rules},
        {"role": "system",
            "content": f"Context: {context}"}
    ]
    
    # Add history messages
    messages.extend(get_history(number))
    
    # Add current user message
    messages.append({
        "role": "user",
        "content": message
    })
    
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return completion.choices[0].message

# Function to send an SMS
def send_sms(number, message):
    try:
        response = requests.post(
            f'{sms_base_url}/gateway/devices/{SMS_DEVICE_ID}/send-sms',
            json={
                'recipients': [number],
                'message': message
            },
            headers={'x-api-key': SMS_API_KEY}
        )
        logger("SMS Sent", f"Message to {number}: {message}")
    except requests.RequestException as e:
        logger("SMS Error", f"Failed to send message to {number}: {str(e)}")
        return {"error": str(e)}

# Function to read the SMS
def read_sms(data):
    pass

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    print(f"Received payload: {payload}")
    number = payload.get('sender')
    message = payload.get('message')
    # check if the number is authorized to chat
    if check_auth(number):
        response = ask_ai(number, message).content
        edit_history(number, datetime.datetime.now(), "user", message)
        edit_history(number, datetime.datetime.now(), "assistant", response)
        logger("Success", f"Successful exchange with {number}")
        send_sms(number, response)
    # if the number is not authorized, send a message to the user
    else:
        logger("Unauthorized", f"The unauthorized number {number} tried to join this service.")
    return jsonify({'status': 'received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=432)