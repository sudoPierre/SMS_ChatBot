from openai import OpenAI
import os.path
import serial
import datetime

API_KEY = PERPLEXITY_API_KEY
client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")
""" ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=1
) """
path = os.path.dirname(os.path.abspath(__file__))
_done = False

# Function to create a log entry
def log_entry(status, content):
    completePath = os.path.join(path, "log.txt")
    file = open(completePath, "r")
    currentContent = file.read()
    file.close()
    file = open(completePath, "w")
    file.write(f"{datetime.datetime.now()} - {status} : {content}\n{currentContent}")
    file.close()

# Function to edit the history of a conversation
def edit_history(number, message):
    completePath = os.path.join(path, "conv_history/", f"{number}.txt")
    if os.path.isfile(completePath):
        file = open(completePath, "a")
        file.write(f"{message}\n")
        log_entry("History", f"History of {number} edited")
    else:
        file = open(completePath, "x")
        file.write(f"As a French SMS chatbot, continue the conversation naturally using this history:\n")
        log_entry("History", f"History of {number} created")
    file.close()

# Function to get the history of a conversation
def get_history(number):
    completePath = os.path.join(path, "conv_history/", f"{number}.txt")
    if os.path.isfile(completePath):
        file = open(completePath, "r")
        output = file.read()
        file.close()
        return output
    else:
        file = open(completePath, "x")
        file.write(f"As a French SMS chatbot, continue the conversation naturally using this history:\n")
        file.close()
        log_entry("History", f"History of {number} created")
        return "You are a helpful assistant. Use only short french sentences with no formatting."

# Function to check if a number is authorized to chat
def check_auth(number):
    completePath = os.path.join(path, 'authContacts.csv')
    with open(completePath, 'r') as file:
        for line in file:
            if number == line.strip():
                return True
        return False

# Function to ask the AI a question
def ask_ai(number, message):
    completion = client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", "content": f"{get_history(number)} \n **Rules:** \n 1. Respond **only in French** with short, casual replies (1-2 sentences max) \n 2. No formatting (bullet points/emoji/markdown) \n 3. Mirror the user's tone (formal/informal) from the history \n 4. If context is unclear, ask 1 very brief clarifying question \n 5. Never repeat previous answers or greetings \n\n Example of acceptable response:  'Oui, je me souviens de notre discussion sur ça. Tu voulais que je te partage des exemples concrets ?'"},
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
    return completion.choices[0].message

# Function to send an SMS
def sens_sms(number, message):
    print(f"Sending message to {number} : {message}")

# Function to parse the SMS
def sms_parser(data):
    messages = []
    lignes = data.split('\r\n')
    for ligne in lignes:
        if '+CMGL:' in ligne:
            infos = ligne.split(',')
            numero = infos[2].strip('"')
            contenu = lignes[lignes.index(ligne)+1]
            messages.append({
                'numero': numero,
                'contenu': contenu
            })
    return messages

# Function to read the SMS
def read_sms(data):
    """ try:
        ser.write(b'AT+CMGF=1\r\n')
        time.sleep(1)
        
        ser.write(b'AT+CMGL="REC UNREAD"\r\n')
        time.sleep(2)
        
        reponse = ser.read(ser.in_waiting()).decode()
        return sms_parser(reponse)
    
    except Exception as e:
        print(f"Erreur : {str(e)}")
        return [] """

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
        edit_history(number, f"[{datetime.datetime.now()}] User: {message}")
        edit_history(number, f"[{datetime.datetime.now()}] Bot: {response}")
        log_entry("Success", f"Successful exchange with {number}")
        sens_sms(number, response)
    # if the number is not authorized, send a message to the user
    else:
        sens_sms(number, "You are not authorized to chat with this number")
        log_entry("Unauthorized", f"The unauthorized number {number} tried to join this service.")