from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Rasa REST API endpoint
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send_message", methods=["POST"])
def send_message():

    user_message = request.json.get("message")

    payload = {
        "sender": "user",
        "message": user_message
    }

    try:
        response = requests.post(RASA_URL, json=payload)
        response_json = response.json()

        if response_json:
            bot_reply = " ".join([msg.get("text", "") for msg in response_json])
        else:
            bot_reply = "Sorry, I didn't understand that."

    except Exception as e:
        bot_reply = "Error connecting to chatbot server."

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)