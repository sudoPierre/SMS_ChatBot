from openai import OpenAI
import os.path
import datetime
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
API_KEY = os.getenv("LLM_API_KEY")

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

# Function to create a log entry
def log_entry(status, content):
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
        "content": f" [{date.strftime("%Y-%m-%d %H:%M:%S")}] {message}"
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
def sens_sms(number, message):
    print(f"Sending message to {number} : {message}")

# Function to read the SMS
def read_sms(data):
    pass

while not _done :
    number = input("What is the number ? : ")
    message = input("What is the message ? : ")

    # close the program if the user types "exit"
    if message == "exit" :
        log_entry("Exit", "User exited the program.")
        break

    # check if the number is authorized to chat
    if check_auth(number):
        response = ask_ai(number, message).content
        edit_history(number, datetime.datetime.now(), "user", message)
        edit_history(number, datetime.datetime.now(), "assistant", response)
        log_entry("Success", f"Successful exchange with {number}")
        sens_sms(number, response)
    # if the number is not authorized, send a message to the user
    else:
        sens_sms(number, "You are not authorized to chat with this number")
        log_entry("Unauthorized", f"The unauthorized number {number} tried to join this service.")