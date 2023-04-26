from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google.oauth2 import service_account
from google.cloud import dialogflow

app = Flask(__name__)

# Set up Dialogflow API credentials
credentials = service_account.Credentials.from_service_account_file("new.json")
project_id = "premium-client-384820"

# Create a Dialogflow client
client = dialogflow.SessionsClient(credentials=credentials)


# Define Flask endpoint for Twilio webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    # Extract incoming message details from Twilio request
    incoming_message = request.form["Body"]
    incoming_number = request.form["From"]
    session_id = incoming_number
    response = MessagingResponse()

    # Send message to Dialogflow
    session = client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=incoming_message, language_code="en-US"
    )
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = client.detect_intent(session=session, query_input=query_input)

    # Extract response from Dialogflow and send it back to user via Twilio
    response_text = response.query_result.fulfillment_text
    response.message(response_text)
    return str(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
