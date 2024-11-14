document.addEventListener('DOMContentLoaded', () => {
    startDataUpdates();
});

function startDataUpdates() {
    setInterval(() => {
        fetch('/getData', {
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
