document.addEventListener("DOMContentLoaded", () => {
    let profile = document.querySelector('.profile');
    let menu = document.querySelector('.menu');

    profile.onclick = function () {
    menu.classList.toggle('active');
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
  
    let main = document.querySelector('main');
    let table = document.querySelector('.grid_table');
    let edit_form = document.querySelector('form[name=edit_user]');
  
    main.addEventListener('click', (event) => {
      event.preventDefault();
      // Open edit form
      if (event.target.classList.contains('edit_button')) {
        main.dataset.mode = 'editing';
        let column = event.target.previousElementSibling;
        edit_form.querySelector('input[name=email]').value = column.children[1].innerText.trim();
        edit_form.querySelector('input[name=first_name]').value = column.children[2].innerText.trim();
        edit_form.querySelector('input[name=last_name]').value = column.children[3].innerText.trim();
        edit_form.querySelector('input[name=username]').value = column.children[4].innerText.trim();
        edit_form.querySelector('input[name=password]').value = column.children[5].innerText.trim();
        edit_form.dataset.id = column.getAttribute('data-id');
      }
  
      // Close edit form
      if (event.target.classList.contains('cancel_button')) {
        event.preventDefault();
        main.dataset.mode = 'viewing';
      }
  
      // Submit PUT request from the edit form
      if (event.target.classList.contains('save_button')) {
        event.preventDefault();
        const id = edit_form.dataset.id;
        let data = Object.fromEntries(new FormData(edit_form).entries());
        server_request(`/website/customer/${id}`, data, 'PUT', function(response) {
          if (response['success']) {
            let column = table.querySelector(`.column[data-id='${id}']`);
            column.children[1].innerText = data.email;
            column.children[2].innerText = data.first_name;
            column.children[3].innerText = data.last_name;
            column.children[4].innerText = data.username;
            column.children[5].innerText = data.password;
          }
  
          main.dataset.mode = 'viewing';
        });
      }
    });
  
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
  