// JavaScript to toggle the dropdown menu
document.addEventListener('DOMContentLoaded', function () {
  const profileDropdown = document.querySelector('.profile');
  const menu = document.querySelector('.menu');

  profileDropdown.addEventListener('click', function () {
    menu.classList.toggle('hidden');
  });
});
window.onload = function(){
  setInterval(() => {
      document.querySelectorAll('.temperatureValue').forEach(element => {
          const temperature = parseFloat(element.innerText);
          element.innerText = (temperature + (Math.random() - 0.5)).toFixed(1);
      });

      document.querySelectorAll('.humidityValue').forEach(element => {
          const humidity = parseFloat(element.innerText);
          element.innerText = (humidity + (Math.random() - 0.5)).toFixed(1);
      });

      document.querySelectorAll('.currentValue').forEach(element => {
          const current = parseFloat(element.innerText);
          element.innerText = (current + (Math.random() - 0.5)).toFixed(1);
      });
  }, 1000);
}
function server_request(url, data = {}, verb, callback) {
  return fetch(url, {
    credentials: 'same-origin',
    method: verb,
    body: JSON.stringify(data),
    headers: { 'Content-Type': 'application/json' }
  })
    .then(response => response.json())
    .then(response => {
      if (callback)
        callback(response);
    })
    .catch(error => console.error('Error:', error));
}

// Create settings object
const settings = {
  showEditForm: false,
  selectedDongleID: '',
  editedConfiguration: {
    name: '',
    temp_thresh: '',
    shielded: '',
    dongleID: ''
  },
  saveConfiguration(configuration) {
    // Implement the logic to save the edited configuration
    console.log('Saving configuration:', configuration);
    // You can send an HTTP request to your backend API to save the configuration data
  }
};

// Handle logout POST request
document.getElementById("sign-out-link").addEventListener("click", function(event) {
  event.preventDefault(); // Prevents the default anchor behavior (navigating to the href)

  // Perform the sign-out action or any other desired functionality
  server_request('/logout', {}, 'POST', function(response) {
    if (response.session_id === 0) {
      location.replace('/');
    }
  });
});

// Apply settings object to the DOM element
document.addEventListener('alpine:init', () => {
  Alpine.data('settings', () => settings);
});
