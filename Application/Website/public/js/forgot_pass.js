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
    let pass_form = document.querySelector('form[name=forgot_pass]');
    let result = document.querySelector('#result');
    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Handle POST Requests
    pass_form.addEventListener('submit', (event) => {
      // Stop the default form behavior
      event.preventDefault();
  
      // Grab the needed form fields
      const action = pass_form.getAttribute('action');
      const method = pass_form.getAttribute('method');
      const data = Object.fromEntries(new FormData(pass_form).entries());
          server_request(action, data, method, (response) => {
            if(response == "There is no password associated with this email"){
                result.innerHTML = response + ".";
              }
              else if (response == "There is no password associated with this username"){
                result.innerHTML = response + ".";
              }
              else{
                result.innerHTML = "Your password is " + response + ".";
              }
          })
    });
  
  });
  