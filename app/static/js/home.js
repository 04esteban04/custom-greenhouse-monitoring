document.addEventListener('DOMContentLoaded', () => {
    syncStates();
});

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

function toggleLight(room) {
    fetch('/toggleLight', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ room })
    })
    .then(response => response.json())
    .then(data => {
        const lightStates = data.lightStates;
        updateLightButtons(lightStates);
    })
    .catch(error => {
        alert('Error toggling light');
    });
}

function toggleAllLights() {
    fetch('/toggleAllLights', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        updateToggleState(Object.values(data).every(state => state));
        updateLightButtons(data);
    })
    .catch(error => {
        alert('Error toggling all lights');
    });
}

function handleLogout(event) {
    const logoutButton = event.target;
    const logoutUrl = logoutButton.getAttribute('data-url');
    window.location.href = logoutUrl;
}

function updateToggleState(areAllLightsOn) {
    const toggleSwitch = document.getElementById('toggle-all-lights');
    const toggleText = document.querySelector('.toggle-text');
    
    toggleSwitch.checked = areAllLightsOn;
    toggleText.textContent = areAllLightsOn ? 'Turn off all lights' : 'Turn on all lights';
}

function updateLightButtons(lightStates) {
    document.querySelectorAll('.roomButton').forEach(button => {
        const room = button.classList[1]; 
        const isOn = lightStates[room];
        button.classList.toggle('on', isOn);
        button.classList.toggle('off', !isOn);
    });

    const areAllLightsOn = Object.values(lightStates).every(state => state);
    updateToggleState(areAllLightsOn);
}

function updateDoorStates(doorStates) {
    Object.keys(doorStates).forEach(doorKey => {
        const door = document.getElementById(doorKey);
        if (door) {
            const isOpen = doorStates[doorKey];
            door.classList.toggle('on', isOpen);
            door.classList.toggle('off', !isOpen);
        }
    });
}

function syncStates() {
    fetch('/getStates')
        .then(response => response.json())
        .then(data => {
            const lightStates = data.lightStates;
            const doorStates = data.doorStates;

            const areAllLightsOn = Object.values(lightStates).every(state => state);
            updateToggleState(areAllLightsOn);
            updateLightButtons(lightStates);
            updateDoorStates(doorStates);
        })
        .catch(error => {
            console.error('Error fetching states:', error);
        });
}
