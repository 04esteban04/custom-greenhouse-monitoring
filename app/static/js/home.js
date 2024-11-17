let currentRotation = 180; 

document.addEventListener('DOMContentLoaded', () => {
    get_sensor_data();
    set_switch_state();
});

function update_data(){
    fetch('/get_data', {
        method: 'GET'
    })    
    .then(response => response.json())
    .then(data => {
        update_light_info(data);
        update_notifications(data);
    }); 
} 

function update_light_info(data){

    lightInfoButton = document.getElementsByClassName('light-button')[0]
    lightInfoButton.classList.toggle('hidden-info', data.switch_state);
    lightInfoButton.classList.toggle('on', data.light_state);
    lightInfoButton.classList.toggle('off', !data.light_state);
    
    light_icon = document.getElementsByClassName('light-icon')[0];
    light_icon.classList.toggle('on', data.light_state);
    light_icon.classList.toggle('off', !data.light_state);

    lightInfoDisplay = document.getElementsByClassName('light-button-info')[0]
    lightInfoDisplay.classList.toggle('hidden-info', !data.switch_state);

    lightInfoDisplay = document.getElementsByClassName('light-button-info')[0];
    lightInfoDisplay.querySelector('div').classList.toggle('auto-on', data.light_state);
    lightInfoDisplay.querySelector('div').classList.toggle('auto-off', !data.light_state);
    
    if (!data.switch_state && data.light_state){
        currentRotation += 180;
    } else{
        currentRotation = 180;
    }
    
    light_icon.style.transform = `rotate(${currentRotation}deg)`;

}

function update_notifications(data){
    
    const notificationsArea = document.querySelector('.notifications');
    
    if (notificationsArea) {
        notificationsArea.innerHTML = ""; 
        data.notifications.forEach(notification => {
            const notificationElement = document.createElement('div');
            notificationElement.classList.add('notification');
            notificationElement.textContent = notification;
            notificationsArea.appendChild(notificationElement);
        });
    }

}

function get_sensor_data() {
    setInterval(() => {
        fetch('/get_sensor_data', {
                method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
                const temperatureValue = data.currentTemperature;
                const humidityValue = data.currentHumidity;

                const temperatureArea = document.querySelector('.temperature p');
                if (temperatureArea) {
                    temperatureArea.textContent = `${temperatureValue} °C`;
                } else {
                    console.error('Element for temperature display not found');
                }

                const humidityArea = document.querySelector('.humidity p');
                if (humidityArea) {
                    humidityArea.textContent = `${humidityValue} %`;
                } else {
                    console.error('Element for humidity display not found');
                }
                
                update_data();

            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, 5000); 

}

function set_switch_state() {
    const modeSwitch = document.getElementById('modeSwitch');
    const switchState = modeSwitch.checked;

    update_label_colors();

    fetch('/set_switch', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ switch_state: switchState })
    });    

    update_data();

}

function update_label_colors() {
    const modeSwitch = document.getElementById('modeSwitch');
    const manualLabel = document.querySelector('.manual-label');
    const autoLabel = document.querySelector('.auto-label');
    
    if (modeSwitch.checked) {
        manualLabel.style.color = 'black';
        autoLabel.style.color = 'white';
    } else {
        manualLabel.style.color = 'white';
        autoLabel.style.color = 'black';
    }
}

function set_light_button_state() {
    fetch('/set_light_state', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        button = document.getElementsByClassName('light-button')[0]
        button.classList.toggle('on', data.light_state);
        button.classList.toggle('off', !data.light_state);

        light_icon = document.getElementsByClassName('light-icon')[0];
        light_icon.classList.toggle('on', data.light_state);
        light_icon.classList.toggle('off', !data.light_state);

        if (data.light_state) {
            currentRotation += 180;
        } else {
            currentRotation = 180;
        }

        light_icon.style.transform = `rotate(${currentRotation}deg)`;
        
    });

    update_data();
}

function toggle_dropdown() {
    const dropdownMenu = document.getElementById('dropdown-menu');
    dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    dropdownMenu.classList.toggle('hidden');
}

function handle_logout(event) {
    const logoutButton = event.target;
    const logoutUrl = logoutButton.getAttribute('data-url');
    window.location.href = logoutUrl;
}

window.onload = update_label_colors;