from flask import Flask, render_template, request
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = "randomkey"
socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def sessions():
    return render_template("session.html")


def message_received(methods=["GET", "POST"]):
    print("Message received")


@socketio.on('event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print(f"Received event: {json}")
    _, red, green, blue = request.remote_addr.split(".")
    json.update(
        {
            'red': hex(int(red))[2:],
            'green': hex(int(green))[2:],
            'blue': hex(int(blue))[2:]
        }
    )
    socketio.emit("response", json, callback=message_received)


if __name__ == "__main__":
    socketio.run(app, debug=True)
