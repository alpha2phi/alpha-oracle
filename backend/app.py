from boto3.session import Session
from chalice import Chalice
from oracle import Handler, Sender, Storage

app = Chalice(app_name="chalice-chat-example")
app.websocket_api.session = Session()
app.experimental_feature_flags.update([
    'WEBSOCKETS'
])

STORAGE = Storage.from_env()
SENDER = Sender(app, STORAGE)
HANDLER = Handler(STORAGE, SENDER)


@app.on_ws_connect()
def connect(event):
    STORAGE.create_connection(event.connection_id)


@app.on_ws_disconnect()
def disconnect(event):
    STORAGE.delete_connection(event.connection_id)


@app.on_ws_message()
def message(event):
    HANDLER.handle(event.connection_id, event.body)


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
