from flask import Flask, request, render_template
from functions import send_whatsapp_messages, load_tokens
from twilio.rest import Client
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

app = Flask(__name__)
# Load the fine-tuned GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("./scam_generator_model")
tokenizer = GPT2Tokenizer.from_pretrained("./scam_generator_model")

# Twilio credentials
twilio_whatsapp_number = 'whatsapp:+14155238886'
recipient_phone_number = 'whatsapp:+6587506901'

#Declaring file path
file_path = "token.txt"

tokens = load_tokens(file_path)
account_sid = tokens.get("account_sid")
auth_token = tokens.get("auth_token")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_message():
    scam_type = request.form.get('scam_type', 'Scam Message')
    input_prompt = f"{scam_type}: "
    input_ids = tokenizer.encode(input_prompt, return_tensors="pt")
    output = model.generate(
        input_ids,
        min_length=50,
        max_length=100,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )
    generated_message = tokenizer.decode(output[0], skip_special_tokens=True)
    return render_template('index.html', generated_message=generated_message)

@app.route('/send', methods=['POST'])
def send_message():
    phone_number = request.form.get('phone_number')
    message_body = request.form.get('message')
    client = Client(account_sid, auth_token)
    success_message = None
    error_message = None

    try:
        message = client.messages.create(
            from_=twilio_whatsapp_number,
            body=message_body,
            to=f"whatsapp:{phone_number}"
        )
        success_message = "Message sent successfully!"
    except Exception as e:
        error_message = f"Failed to send message. Error: {str(e)}"

    return render_template('index.html', success_message=success_message, error_message=error_message)

@app.route('/control')
def control_center():
    return render_template('control_center.html')


if __name__ == '__main__':
    app.run(debug=True)