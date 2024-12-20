from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Sample user data storage (a text file, database would be better)
users_db = 'users.txt'

@app.route('/')
def home():
    # Check if user is logged in, if not redirect to login page
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Save user data to a file (for simplicity, a file is used here)
        with open(users_db, 'a') as file:
            file.write(f"{username},{password}\n")
        
        return redirect(url_for('login'))  # After registration, redirect to login
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Here, you'd normally check the credentials from a database or a file
        with open(users_db, 'r') as file:
            users = file.readlines()
            for user in users:
                stored_username, stored_password = user.strip().split(',')
                if stored_username == username and stored_password == password:
                    session['username'] = username
                    return redirect(url_for('home'))  # Redirect to home page after login
        
        return "Invalid username or password. Please try again."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route('/exchange')
def exchange():
    # Redirect to exchange page
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('exchange.html')

@app.route('/balance')
def balance():
    # Redirect to balance page
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('balance.html')

@app.route('/balance/<username>')
def get_balance(username):
    # For simplicity, we return dummy data for balance
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'}), 403
    return jsonify({
        'username': username,
        'BTC': 1.5,
        'ETH': 10,
        'USD': 1000
    })

if __name__ == '__main__':
    if not os.path.exists(users_db):
        open(users_db, 'w').close()  # Create the file if it doesn't exist
    app.run(debug=True)
