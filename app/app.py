from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "cR/N{E{4Ta#qUn5"

storedUsername = "admin"
storedPassword = "admin123"

hashedPassword = bcrypt.hashpw(storedPassword.encode('utf-8'), bcrypt.gensalt())

photo_path = "./static/images/house.jpg"

temperature = [
    22.5, 23.0, 22.8, 23.5, 24.0, 23.2, 22.9, 23.3, 23.1, 22.7,
    23.6, 23.4, 23.0, 22.9, 23.3, 23.5, 23.2, 22.8, 23.1, 23.4,
    23.0, 22.7, 23.3, 23.6, 23.2, 22.9, 23.5, 23.1, 22.6, 23.4,
    23.7, 22.8, 23.3, 23.0, 23.5, 23.2, 22.9, 23.4, 23.6, 23.1,
    23.5, 23.0, 22.8, 23.2, 23.3, 22.7, 23.1, 23.4, 23.5, 22.9,
    23.6, 23.0, 23.2, 23.1, 23.7, 23.3, 22.9, 23.4, 23.0, 22.8,
    23.3, 23.1, 23.5, 22.9, 23.4, 23.2, 23.0, 23.7, 22.8, 23.3,
    23.4, 22.9, 23.1, 23.5, 23.2, 23.0, 23.3, 22.8, 23.1, 23.4,
    23.6, 23.2, 23.0, 22.9, 23.1, 23.3, 23.5, 22.7, 23.2, 23.4,
    23.0, 22.9, 23.1, 23.3, 23.5, 22.8, 23.4, 23.6, 23.1, 22.7
]

humidity = [
    45, 50, 48, 52, 47, 49, 46, 51, 47, 48,
    49, 46, 52, 50, 47, 48, 51, 45, 50, 48,
    49, 47, 46, 50, 52, 48, 47, 49, 51, 46,
    50, 47, 49, 48, 46, 52, 45, 51, 48, 47,
    49, 46, 51, 45, 50, 47, 48, 49, 52, 46,
    50, 48, 47, 49, 51, 45, 52, 47, 48, 49,
    50, 46, 52, 45, 49, 48, 51, 47, 46, 50,
    47, 49, 52, 48, 45, 50, 47, 49, 48, 46,
    52, 50, 47, 49, 51, 46, 48, 52, 45, 50,
    49, 48, 47, 51, 46, 52, 50, 48, 49, 45
]

data_index = 0

# Basic routes
@app.route('/')
def index():
    if 'userSession' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'userSession' in session:
        return redirect(url_for('home'))

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == storedUsername and bcrypt.checkpw(password.encode('utf-8'), hashedPassword):
            session['userSession'] = {'username': username}
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/home')
def home():
    if 'userSession' in session:
        return render_template(
            'home.html',
            photoUrl = None,
            currentTemperature="---",
            currentHumidity="---",
            avgTempValue="---",
            avgHumValue="---"
        )
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('userSession', None)
    return redirect(url_for('login'))


# Functionality routes
@app.route('/getData', methods=['GET'])
def get_data():
    global data_index

    current_temperature = temperature[data_index]
    current_humidity = humidity[data_index]

    data_index = (data_index + 1) % len(temperature)

    return jsonify(currentTemperature=current_temperature, currentHumidity=current_humidity)

@app.route('/getAvgData', methods=['GET'])
def get_avg_data():
    # Calcular los promedios de temperatura y humedad
    avg_temperature = sum(temperature) / len(temperature) if temperature else 0
    avg_humidity = sum(humidity) / len(humidity) if humidity else 0

    return jsonify(avgTempValue=round(avg_temperature, 2), avgHumValue=round(avg_humidity, 2))

@app.route('/takePhoto', methods=['POST'])
def takePhoto():
    if os.path.exists(photo_path):
        return send_file(photo_path, mimetype='image/jpeg')
    else:
        return jsonify({"error": "Photo not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
