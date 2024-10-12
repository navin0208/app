from flask import Flask, send_from_directory, render_template, jsonify, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)  # Initialize SocketIO

users = {
    "admin": "decon123"
}

pi_data = {}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('protected'))
    else:
        flash('Wrong Password or Username')
        return redirect(url_for('home'))

@app.route('/protected')
def protected():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('home'))

# Endpoint to receive data from Raspberry Pis
@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json
    pi_id = data.get('pi_id')
    product_count = data.get('product_count')
    not_ok_count = data.get('not_ok_count')
    shift = data.get('shift')

    # Store the data received from the Raspberry Pi
    pi_data[pi_id] = {
        'product_count': product_count,
        'not_ok_count': not_ok_count,
        'shift': shift
    }

    # Emit real-time updates to connected clients
    socketio.emit('update_data', pi_data)

    return jsonify({'status': f'Data received from {pi_id}'})

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(pi_data)

@app.route('/download_data', methods=['GET'])
def download_data():
    df = pd.DataFrame.from_dict(pi_data, orient='index')
    file_path = 'raspberry_pi_data.xlsx'
    df.to_excel(file_path, index=True)
    return send_from_directory(os.getcwd(), file_path, as_attachment=True)

@app.route('/Images/<path:filename>')
def serve_image(filename):
    return send_from_directory('Images', filename)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
