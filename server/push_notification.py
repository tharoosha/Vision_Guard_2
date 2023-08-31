import firebase_admin
from firebase_admin import credentials, messaging

# Initialize Firebase with your credentials
cred = credentials.Certificate('path/to/your/credentials.json')
firebase_admin.initialize_app(cred)

def send_push_notification(device_token, message_body):
    # Send a push notification to the specified device token
    message = messaging.Message(
        data={
            'title': 'CCTV Alert',
            'body': message_body,
        },
        token=device_token,
    )

    response = messaging.send(message)
    print(f'Successfully sent message: {response}')
    
if __name__ == "__main__":
    # Replace 'device_token_user1' with the actual device token
    send_push_notification('device_token_user1', 'Human Action Detected')
