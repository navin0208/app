from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)  # Initialize SocketIO

# Store data from Raspberry Pi
pi_data = {}

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to receive data from Raspberry Pis
@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json
    pi_id = data.get('pi_id')
    product_count = data.get('product_count')
    not_ok_count = data.get('not_ok_count')
    shift = data.get('shift')

    # Store the data received from Raspberry Pi
    pi_data[pi_id] = {
        'product_count': product_count,
        'not_ok_count': not_ok_count,
        'shift': shift
    }

    # Emit real-time updates to connected clients
    socketio.emit('update_data', pi_data)

    return jsonify({'status': f'Data received from {pi_id}'})

# Serve the stored data to the frontend
@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(pi_data)

# Run the Flask-SocketIO app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
