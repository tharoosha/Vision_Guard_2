from flask import Flask, request
from database import store_event, store_notification
from flask import jsonify

app = Flask(__name__)

# @app.route('/', methods = ['GET'])
# def get_articles():
#     return jsonify({"Hello":"World"})


# if __name__ == "__main__":
#     app.run(debug=True)


@app.route('/handle_event', methods=['POST'])
def handle_event():
    data = request.json
    camera_id = data['camera_id']
    event_type = data['event_type']
    timestamp = data['timestamp']

    store_event(camera_id, event_type, timestamp)
    # ... send notifications, return response, etc.

if __name__ == "__main__":
    app.run()
