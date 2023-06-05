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
    // References to frequently accessed elements
    let user_form = document.querySelector('form[name=forgot_user]');
    let result = document.querySelector('#result');
    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Handle POST Requests
    user_form.addEventListener('submit', (event) => {
      // Stop the default form behavior
      event.preventDefault();
  
      // Grab the needed form fields
      const action = user_form.getAttribute('action');
      const method = user_form.getAttribute('method');
      const data = Object.fromEntries(new FormData(user_form).entries());

          server_request(action, data, method, (response) => {
            if(response == "There is no username associated with this email"){
              result.innerHTML = response + ".";
            }
            else if (response == "Not a valid email"){
              result.innerHTML = response + ".";
            }
            else{
              result.innerHTML = "Your username is " + response + ".";
            }
          })
    });
  
  });
  