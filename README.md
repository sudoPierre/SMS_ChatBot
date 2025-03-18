# Raspberry Pi AI Chatbot via SIM800L  

## Description  
This project is a Python-based chatbot running on a Raspberry Pi, allowing communication with an AI (Perplexity) via SMS using a SIM800L module. It maintains conversation history for a fluid user experience and includes an authorization system to restrict access to approved contacts. A logging system is also implemented to facilitate debugging.  

⚠ **Note:** This is a prototype and may not always work as expected. Additionally, it operates on the 2G network, which is being phased out in some countries.  

## Features  
- **AI Communication:** Uses Perplexity AI to generate responses.  
- **Conversation History:** Stored in the `conv_history` folder for continuous interaction.  
- **Authorized Contacts:** Only numbers listed in `authContacts.csv` can interact with the chatbot.  
- **Logging System:** `log.txt` records interactions and errors for debugging.  

## Requirements  
- Raspberry Pi (tested on Raspberry Pi 3 Model B)  
- SIM800L module  
- Minicom installed (`sudo apt install minicom`)  
- Python 3.x  
- A working 2G SIM card  

## Installation & Setup  
1. **Connect the SIM800L module** to your Raspberry Pi properly. Follow this tutorial for wiring and configuration:  
   [SIM800L Raspberry Pi Setup Guide](https://howtoraspberrypi.com/sim800l-gsm-gps-raspberry-2/)  
2. **Install dependencies:**  
   ```bash
   pip install openai pyserial
   ```  
3. **Set up the API key:**  
   - Replace `API_KEY = PERPLEXITY_API_KEY` in `main.py` with your Perplexity API key.  
4. **Run the script:**  
   ```bash
   python main.py
   ```  

## How It Works  
1. The script checks if an incoming SMS is from an authorized contact.  
2. If authorized, the message is sent to Perplexity AI, using conversation history for context.  
3. The AI's response is logged and sent back via SMS.  
4. If unauthorized, the user receives a rejection message.  

## Troubleshooting  
- Ensure the SIM800L module is correctly connected and powered.  
- Verify your SIM card supports 2G and is activated.  
- Check `log.txt` for errors.  

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
sudoPierre
