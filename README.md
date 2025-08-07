# SMS ChatBot (Powered by TextBee.dev)

A Python-based SMS chatbot that leverages the [TextBee.dev](https://textbee.dev) SMS Gateway and its webhook feature to receive and respond to SMS messages using Perplexity AI. The bot supports message history, sender whitelisting, and logging.

This project is now fully cloud-based — no need for GSM hardware or Raspberry Pi.

---

## Features

- ⚡️ Instantly responds to incoming SMS messages via webhook
- 💬 Supports message history per sender for contextual responses
- ✅ Sender whitelist (only authorized numbers can interact with the bot)
- 🧠 Uses Perplexity AI to generate intelligent replies
- 📝 Simple logging system to monitor activity
- 🛠️ Easy to configure and run with a `.env` file

---

## Warning

This project is a **prototype** and should not be used in production without proper security and validation measures.

**Note:** The previous version using the SIM800L module and Raspberry Pi has been deprecated in favor of the [TextBee.dev](https://textbee.dev) SMS Gateway.

---

## How It Works

1. A user sends an SMS to your TextBee number.
2. TextBee forwards the message to your hosted webhook.
3. The webhook receives and processes the SMS.
4. The chatbot queries Perplexity AI and generates a response.
5. The response is sent back to the user via TextBee.

---

## Logs

The bot logs the following information:
- Incoming phone numbers and messages
- Timestamps of interactions
- AI responses

All logs are stored in the local `logs/` directory (one file per session or day depending on configuration).

---

## License

This project is released under the MIT License.  
You are free to use, modify, and distribute it.

---

## Disclaimer

Use this tool responsibly. SMS costs may apply depending on your TextBee plan. Make sure to comply with privacy laws and obtain consent before storing or processing users' phone numbers and messages.

---

## Links

- [TextBee.dev](https://textbee.dev) – SMS Gateway provider
- [Perplexity.ai](https://www.perplexity.ai/) – AI answering engine
- [Project Repository](https://github.com/sudoPierre/SMS_ChatBot)
