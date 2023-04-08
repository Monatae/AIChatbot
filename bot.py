from twilio.rest import Client
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
import os

# Set up the Twilio client
account_sid = "AC81c0755065e9eba6542ca94a9571ca8e"
auth_token = "63a4d1fa607bc9ef2fa7b1525bb3a6a7"
client = Client(account_sid, auth_token)

# Set up the Dialogflow client
DIALOGFLOW_PROJECT_ID = "ordinal-gear-381907"
DIALOGFLOW_LANGUAGE_CODE = "en"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ordinal-gear-381907-452922c5eb30.json"
session_client = dialogflow.SessionsClient()


# Define a function to process incoming WhatsApp messages
def process_message(from_number, body):
    # Set up the Dialogflow session
    session_id = f"whatsapp-{from_number}"
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

    # Send the user's message to Dialogflow
    text_input = dialogflow.TextInput(text=body, language_code=DIALOGFLOW_LANGUAGE_CODE)
    # Making a query using against dialogflow out of the text
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        # detecting intent of the query
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
    """
    so the logic of our app is:

    when end-user sends a whatsapp message to our twilio sandbox, twilio makes an HTTP POST call to our application



        1. You call this webhook via the webhook's endpoint placed in Twilio (URL --> in this case it is a HTTP POST request on the flaskapp's address, port number and its flaskapp route name)
        2. The webhook then strips some details from the HTTP POST request's body i.e from number and body of the request
        3. The webhook then takes the from-phonenumber and the body of the message for processing
        4. The from-phonenumber is used to create a unique session ID while the body is used to generate queries against google diaglog flow
        5. The webhook then takes the response which is returned by the querying the google dialog flow from point [4], and sends it as a message back to the from-phone number
        6. After executing the above 5 steps, the webhook returns OK as an HTTP status code

    the end
    """
    # Parse the incoming Twilio message from the http post request using request lib
    from_number = request.form["From"]
    body = request.form["Body"]

    # Process the message using Dialogflow
    response = process_message(from_number, body)

    # Send the response back to the user
    send_message(from_number, response)

    return "OK"


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5001)
