from twilio.rest import Client
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
import os

# Set up the Twilio client
account_sid = "YOUR_ACCOUNT_SID"
auth_token = "YOUR_AUTH_TOKEN"
client = Client(account_sid, auth_token)

# Set up the Dialogflow client
DIALOGFLOW_PROJECT_ID = "YOUR_PROJECT_ID"
DIALOGFLOW_LANGUAGE_CODE = "en"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
session_client = dialogflow.SessionsClient()


# Define a function to process incoming WhatsApp messages
def process_message(from_number, body):
    # Set up the Dialogflow session
    session_id = f"whatsapp-{from_number}"
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

    # Send the user's message to Dialogflow
    text_input = dialogflow.TextInput(text=body, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(
            session=session, query_input=query_input
        )
    except InvalidArgument:
        # Handle any errors from Dialogflow
        return "I'm sorry, I didn't understand that."

    # Get the Dialogflow response
    if response.query_result.intent.is_fallback:
        return "I'm sorry, I didn't understand that."
    else:
        return response.query_result.fulfillment_text


# Define a function to send a message back to the user
def send_message(to_number, message):
    message = client.messages.create(
        body=message, from_="whatsapp:+14155238886", to=f"whatsapp:{to_number}"
    )
    return message.sid


# Set up a Flask app to receive incoming messages from Twilio
from flask import Flask, request

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    # Parse the incoming Twilio message
    from_number = request.form["From"]
    body = request.form["Body"]

    # Process the message using Dialogflow
    response = process_message(from_number, body)

    # Send the response back to the user
    send_message(from_number, response)

    return "OK"


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
