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

function generateUUID() {
  // Generate a version 4 UUID
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // Define the 'request' function to handle interactions with the server
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

  // References to frequently accessed elements
  let add_form = document.querySelector('form[name=add_user]');
  let result = document.querySelector('#result');

  // Handle POST Requests
  add_form.addEventListener('submit', (event) => {
    // Stop the default form behavior
    event.preventDefault();

    // Grab the needed form fields
    const action = add_form.getAttribute('action');
    const newAction = "/website/check_customer";
    const method = add_form.getAttribute('method');
    const data = Object.fromEntries(new FormData(add_form).entries());
    
    // Generate a UUID for the request
    const UUID = generateUUID();
    
    server_request(newAction, data, method, (response) => {
      if (response === "verified") {
        const url = `${action}/${UUID}`;
        server_request(url, data, method, (response) => {
          location.replace('/');
        });
      } else if (response === "username") {
        result.innerHTML = "The username is already taken!";
      } else if (response === "email") {
        result.innerHTML = "The email is already taken!";
      } else if (response === "dongleID") {
        result.innerHTML = "This product is already in use.";
      } else if (response === "all") {
        result.innerHTML = "You already have an account with the same username, email, and product ID.";
      }
    });
  });
});
