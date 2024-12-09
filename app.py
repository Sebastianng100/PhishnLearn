from flask import Flask, request, render_template
from functions import send_whatsapp_messages, load_tokens
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials
twilio_whatsapp_number = 'whatsapp:+14155238886'
recipient_phone_number = 'whatsapp:+6587506901'

#Declaring file path
file_path = "token.txt"

tokens = load_tokens(file_path)
account_sid = tokens.get("account_sid")
auth_token = tokens.get("auth_token")


@app.route('/', methods=['GET', 'POST'])
def index():
    success_message = None
    error_message = None
    if request.method == 'POST':
        # Get the message from the form
        message_body = request.form.get('message')
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send the message
        try:
            message = client.messages.create(
                from_=twilio_whatsapp_number,
                body=message_body,
                to=recipient_phone_number
            )
            success_message = "Message sent successfully!"
        except Exception as e:
            error_message = f"Failed to send message. Error: {str(e)}"
    
    return render_template('index.html', success_message=success_message, error_message=error_message)

@app.route('/control')
def control_center():
    chart1_data = {'clicked': 30, 'ignored': 70}  # Example data
    chart2_data = {'clicked': 8, 'ignored': 92}   # Example data
    return render_template('control_center.html', chart1_data=chart1_data, chart2_data=chart2_data)


if __name__ == '__main__':
    app.run(debug=True)