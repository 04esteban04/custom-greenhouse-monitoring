from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "cR/N{E{4Ta#qUn5"

storedUsername = "admin"
storedPassword = "admin123"

hashedPassword = bcrypt.hashpw(storedPassword.encode('utf-8'), bcrypt.gensalt())

photo_path = "./static/images/house.jpg"

temperature = [22.5, 23.0, 22.8, 23.5]

humidity = [45, 50, 48, 52, 47]

data_index = 0

switch_state = False
light_state = False

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
            avgHumValue="---",
            switch_state=switch_state,
            light_state=light_state
        )
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('userSession', None)
    return redirect(url_for('login'))


# Functionality routes

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(switch_state=switch_state, light_state=light_state)

@app.route('/update_switch', methods=['POST'])
def update_switch():
    global switch_state
    switch_state = request.json.get('switch_state', False)
    return jsonify(success=True)

@app.route('/get_light_state', methods=['GET'])
def get_light_state():
    return jsonify(light_state=light_state)

@app.route('/update_light_state', methods=['POST'])
def update_light_state():
    global light_state
    light_state = not light_state
    return jsonify(light_state=light_state)

@app.route('/get_sensor_data', methods=['GET'])
def get_sensor_data():
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
