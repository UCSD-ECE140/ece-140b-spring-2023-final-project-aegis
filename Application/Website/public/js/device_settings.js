      // JavaScript to toggle the dropdown menu
      document.addEventListener('DOMContentLoaded', function () {
        const profileDropdown = document.querySelector('.profile');
        const menu = document.querySelector('.menu');
        
        profileDropdown.addEventListener('click', function () {
          menu.classList.toggle('hidden');
        });
    
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

      
  });
  