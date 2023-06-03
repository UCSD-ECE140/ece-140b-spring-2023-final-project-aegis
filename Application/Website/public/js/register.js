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
    let add_form = document.querySelector('form[name=add_user]');
    let result = document.querySelector('#result');
    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Handle POST Requests
    add_form.addEventListener('submit', (event) => {
      // Stop the default form behavior
      event.preventDefault();
  
      // Grab the needed form fields
      const action = add_form.getAttribute('action');
      const newAction = "/check_customer";
      const method = add_form.getAttribute('method');
      const data = Object.fromEntries(new FormData(add_form).entries());
      server_request(newAction, data, method, (response) => {
        if(response === "verified"){
          server_request(action, data, method, (response) => {
            location.replace('/home');
          })
        }
        else if(response === "username"){
          result.innerHTML = "The username is already taken!";
        }
        else if (response === "email"){
          result.innerHTML = "The email is already taken!";
        }
        else if (response === "dongleID"){
            resultinnerHTML = "This product is already in use."
        }
        else if (response === "all"){
            result.innerHTML = "You already have an account with the same username, email. and product id."
        }
      })
    });
  
  });
  