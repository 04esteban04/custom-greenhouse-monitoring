from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import bcrypt
import spidev

app = Flask(__name__)
app.secret_key = "cR/N{E{4Ta#qUn5"

storedUsername = "admin"
storedPassword = "admin123"

hashedPassword = bcrypt.hashpw(storedPassword.encode('utf-8'), bcrypt.gensalt())

spi = None

temperature = [15.0, 18.5, 22.0, 23.1, 23.5, 25.0, 28.0, 30.5, 33.0, 35.0]
humidity = [85, 78, 72, 65, 55, 50, 45, 40, 30, 25]
data_index = 0

switch_state = False
light_state = False

notifications = ["General status: ---", 
                "Temperature status: ---",
                "Humidity status: ---", 
                "Light status: ---"]

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
    global spi

    if 'userSession' in session:
        
        spi = set_SPI_config()

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
    return jsonify(
        switch_state=switch_state, 
        light_state=light_state,
        notifications=notifications)

@app.route('/get_sensor_data', methods=['GET'])
def get_sensor_data():
    global data_index, spi
    
    sensor_humidity = read_sensor()
    
    if (spi is not None and sensor_humidity is not None):
        current_humidity = sensor_humidity
    else:
        current_humidity = humidity[data_index]

    current_temperature = temperature[data_index]
    data_index = (data_index + 1) % len(temperature)

    set_notifications(current_temperature, current_humidity)

    return jsonify(
        currentTemperature=current_temperature, 
        currentHumidity=current_humidity)

@app.route('/set_switch', methods=['POST'])
def set_switch():
    global switch_state
    switch_state = request.json.get('switch_state', False)
    return jsonify(success=True)

@app.route('/set_light_state', methods=['POST'])
def set_light_state():
    global light_state
    light_state = not light_state
    return jsonify(light_state=light_state)

# Helper functions
def set_notifications(current_temperature, current_humidity):
    notifications[0] = f"General status: All systems operational."
    if current_temperature < 20:
        notifications[1] = f"Temperature status: Low ({current_temperature} °C). Consider turning on the lights."
    elif current_temperature > 30:
        notifications[1] = f"Temperature status: High ({current_temperature} °C). Monitor closely."
    else:
        notifications[1] = f"Temperature status: Optimal ({current_temperature} °C)."

    if current_humidity < 40:
        notifications[2] = f"Humidity status: Low ({current_humidity} %). Consider watering the plants."
    elif current_humidity > 70:
        notifications[2] = f"Humidity status: High ({current_humidity} %). Consider draining water."
    else:
        notifications[2] = f"Humidity status: Optimal ({current_humidity} %)."

    notifications[3] = f"Light status: {'On' if light_state else 'Off'}."

def set_SPI_config():
    try:
        spi = spidev.SpiDev()
        spi.open(0, 0)  # bus 0, device 0
        spi.max_speed_hz = 1350000
        return spi
    except:
        return None

def read_sensor():
    global spi

    try:
        adc_channel = 0 
        adc_response = spi.xfer2([1, (8 + adc_channel) << 4, 0])  
        raw_value = ((adc_response[1] & 3) << 8) + adc_response[2]
        
        if (raw_value < 277):
            humidity_percentage = 80
        elif (277 < raw_value < 380):
            humidity_percentage = 50
        else:
            humidity_percentage = 30
            
        return humidity_percentage

    except:
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
