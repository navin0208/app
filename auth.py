from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for security

# Hardcoded user credentials
users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3",
    "user4": "password4",
    "user5": "password5",
    "user6": "password6",
    "user7": "password7",
    "user8": "password8",
    "user9": "password9",
    "user10": "password10"
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('protected'))  # Redirect to the protected page
    else:
        flash('Invalid credentials. Please try again.')
        return redirect(url_for('home'))

@app.route('/protected')
def protected():
    if 'username' in session:
        return render_template('http://127.0.0.1:5000/', username=session['username'])
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(port=8080, debug=True)  # Run on port 8080
