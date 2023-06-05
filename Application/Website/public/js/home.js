document.addEventListener("DOMContentLoaded", () => {

    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Define the 'request' function to handle interactions with the server
    function server_request(url, data={}, verb, callback) {
      return fetch(url, {
        credentials: 'same-origin',
        method: verb,
        body: JSON.stringify(data),
        headers: {'Content-Type': 'application/json'}
      })
      .then(response => response.json())
      .then(response => {
        if(callback)
          callback(response);
      })
      .catch(error => console.error('Error:', error));
    }
  
    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Handle Login POST Request
    let login_form = document.querySelector('form[name=login_form]');
    let result = document.querySelector('#result');
    let count = 0;
    if (login_form) { // in case we are not on the login page
      login_form.addEventListener('submit', (event) => {
        // Stop the default form behavior
        event.preventDefault();
  
        // Grab the needed form fields
        const action = login_form.getAttribute('action');
        const method = login_form.getAttribute('method');
        const data = Object.fromEntries(new FormData(login_form).entries());
        // Submit the POST request
        server_request(action, data, method, (response) => {
          if (response.session_id != 0) {
            location.replace('/profile');
          }
          else{
            text = count < 3 ? "Incorrect username or password.<br>Please check your login credentials and try again." : "If you have forgotten your password, you can reset it using the \"Forgot Password\" link below.<br><br>If you continue to have trouble logging in, please contact support for assistance.";
            result.innerHTML = text;
          }
          count++;
        });
      });
    }

  });