function server_request(url, data = {}, verb, UUID, callback) {
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

function handleLoginSubmit(event) {
  event.preventDefault();

  const login_form = document.querySelector('form[name=login_form]');
  const action = login_form.getAttribute('action');
  const method = login_form.getAttribute('method');
  const data = Object.fromEntries(new FormData(login_form).entries());

  let UUID = null;
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim().split('=');
    if (cookie[0] === 'deviceID') {
      UUID = cookie[1];
      break;
    }
  }

  if (!UUID) {
    UUID = generateUUID();
    // Set the generated UUID as a cookie
    document.cookie = `deviceID=${UUID}`;
  }

  const url = `${action}/${UUID}`;

  server_request(url, data, method, UUID, (response) => {
    const result = document.querySelector('#result');
    let count = 0;
    if (response.session_id != 0) {
      location.replace('/profile');
    } else {
      const text = count < 3 ? "Incorrect username or password.<br>Please check your login credentials and try again." : "If you have forgotten your password, you can reset it using the \"Forgot Password\" link below.<br><br>If you continue to have trouble logging in, please contact support for assistance.";
      result.innerHTML = text;
    }
    count++;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const login_form = document.querySelector('form[name=login_form]');
  if (login_form) {
    login_form.addEventListener('submit', handleLoginSubmit);
  }
});
