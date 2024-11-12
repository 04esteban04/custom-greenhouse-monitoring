from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
import bcrypt
import os
#import ctypes

app = Flask(__name__)
app.secret_key = "cR/N{E{4Ta#qUn5"

storedUsername = "admin"
storedPassword = "admin123"

hashedPassword = bcrypt.hashpw(storedPassword.encode('utf-8'), bcrypt.gensalt())

photo_path = "./static/images/house.jpg"

"""
lib_path = os.path.join(os.path.dirname(__file__), "/usr/lib/libcontrol.so.0")
lib = ctypes.CDLL(lib_path)
#lib = ctypes.CDLL('/usr/lib/libcontrol.so.0')
# ../lib/.libs/libcontrol.so

lib.setPinMode.argtypes = [ctypes.c_int, ctypes.c_char_p]
lib.setPullMode.argtypes = [ctypes.c_int, ctypes.c_char_p]
lib.digitalWrite.argtypes = [ctypes.c_int, ctypes.c_char_p]
lib.digitalRead.restype = ctypes.c_int
lib.digitalRead.argtypes = [ctypes.c_int]
lib.blink.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
"""

roomPins = {
    "livingRoom": 15,
    "diningRoom": 17,
    "kitchen": 27,
    "room1": 22,
    "room2": 23
}

doorPins = {
    "mainDoor": 24,
    "backDoor": 25,
    "room1Door": 5,
    "room2Door": 6
}

lightStates = {
    "livingRoom": False,
    "diningRoom": False,
    "kitchen": False,
    "room1": False,
    "room2": False
}

doorStates = {
    "mainDoor": False,
    "backDoor": False,
    "room1Door": False,
    "room2Door": False
}

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

        """
        TODO:

            An array or dictionary must be created in server to stored the pins 
            used in hardware to make reference to any light and door.

            The function digitalRead(pinNumber) from library must be used 
            to get the lights and doors states from hardware.

            After that, all the lights and doors states from server have to 
            be updated correspondingly
        
        """

        return render_template(
            'home.html',
            lightStates = lightStates,
            doorStates = doorStates,
            photoUrl = None  
        )
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('userSession', None)
    return redirect(url_for('login'))


# Functionality routes
@app.route('/getStates', methods=['GET'])
def get_states():

    """
    for room in lightStates:
        pin = roomPins[room]  
        hardware_state = lib.digitalRead(pin) 
        lightStates[room] = True if hardware_state == 1 else False  

    for door in doorStates:
        pin = doorPins[door] 
        hardware_state = lib.digitalRead(pin) 
        doorStates[door] = True if hardware_state == 1 else False  
    """

    responseData = {
        "lightStates": lightStates,
        "doorStates": doorStates
    }

    return jsonify(responseData)
    
@app.route('/toggleLight', methods=['POST'])
def toggleLight():
    
    data = request.json
    room = data.get('room')
    
    if room in lightStates:
        
        lightStates[room] = not lightStates[room]

        """
        pin = roomPins[room]
        lib.setPinMode(pin, b'op')

        if lightStates[room]:
            lib.digitalWrite(pin, b"dh") 
        else:
            lib.digitalWrite(pin, b"dl")  
        """

        return jsonify({"lightStates": lightStates})
    else:
        return jsonify({"error": "Invalid room"}), 400

@app.route('/toggleAllLights', methods=['POST'])
def toggleAllLights():

    all_on = all(lightStates.values())

    if all_on:
        for room in lightStates:
            lightStates[room] = not all_on
            """
            pin = roomPins[room]
            lib.setPinMode(pin, b'op')
            lib.digitalWrite(pin, b"dl")
            """
    else: 
        for room in lightStates:
            lightStates[room] = True
            """
            pin = roomPins[room]
            lib.setPinMode(pin, b'op')
            lib.digitalWrite(pin, b"dh")
            """
            
    return jsonify(lightStates)

@app.route('/takePhoto', methods=['POST'])
def takePhoto():
    if os.path.exists(photo_path):
        return send_file(photo_path, mimetype='image/jpeg')
    else:
        return jsonify({"error": "Photo not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
