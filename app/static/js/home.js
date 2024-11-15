document.addEventListener('DOMContentLoaded', () => {
    /* startDataUpdates(); */
    getData();
});

function getData(){
    fetch('/get_data', {
        method: 'GET'
    })    
    .then(response => response.json())
    .then(data => {
        lightInfoButton = document.getElementsByClassName('light-button')[0]
        lightInfoButton.classList.toggle('hidden-info', data.switch_state);

        lightInfoDisplay = document.getElementsByClassName('light-button-info')[0]
        lightInfoDisplay.classList.toggle('hidden-info', !data.switch_state);

        lightInfoDisplay.querySelector('p').textContent = data.light_state;
    });
} 

function startDataUpdates() {
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
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, 5000); 
}

function updateSwitchState() {
    const modeSwitch = document.getElementById('modeSwitch');
    const switchState = modeSwitch.checked;

    updateLabelColors();

    fetch('/update_switch', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ switch_state: switchState })
    });    

    getData();
}

function updateLabelColors() {
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

function updateLightButtonState() {
    fetch('/update_light_state', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        button = document.getElementsByClassName('light-button')[0]
        button.classList.toggle('on', data.light_state);
        button.classList.toggle('off', !data.light_state);
    });
}

function toggleDropdown() {
    const dropdownMenu = document.getElementById('dropdown-menu');
    dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    dropdownMenu.classList.toggle('hidden');
}

function handleLogout(event) {
    const logoutButton = event.target;
    const logoutUrl = logoutButton.getAttribute('data-url');
    window.location.href = logoutUrl;
}

function takePhoto() {
    fetch('/takePhoto', {
        method: 'POST'
    })
    .then(response => response.blob())
    .then(blob => {
        const imageObjectURL = URL.createObjectURL(blob);
        document.querySelector('.photo-logo').src = imageObjectURL;
    })
    .catch(error => {
        alert('Error taking photo');
    });
}

function getAvgData() {
    fetch('/getAvgData', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            if (data) {
                const avgTemperatureValue = data.avgTempValue;
                const avgHumidityValue = data.avgHumValue;

                const avgTemperatureArea = document.querySelector('.average-info .avg-temperature p');
                if (avgTemperatureArea) {
                    avgTemperatureArea.textContent = `${avgTemperatureValue} °C`;
                }

                const avgHumidityArea = document.querySelector('.average-info .avg-humidity p');
                if (avgHumidityArea) {
                    avgHumidityArea.textContent = `${avgHumidityValue} %`;
                }
            }
        })
        .catch(error => {
            console.error('Error fetching average data:', error);
        });
}

window.onload = updateLabelColors;